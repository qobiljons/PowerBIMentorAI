from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .models.gemini import Gemini
from PowerBIMentor.utils.processor import analyze_pbit
from PowerBIMentor.utils.checker import get_file_by_type
from PowerBIMentor.utils.extractor import extract_zip_to_temp


class PowerBIMentor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp", model: Optional[Gemini] = None):
        if model is None:
            model = Gemini(api_key=api_key, model_name=model_name)
        self.model = model

    def _prepare_answer_path(self, answer_path: str) -> str:
        path = Path(answer_path).resolve()

        if not path.exists():
            raise FileNotFoundError(
                f"Submission path not found: {answer_path}\n"
                f"Resolved to: {path}\n"
                f"Current working directory: {Path.cwd()}\n"
                f"Please check that the path is correct."
            )

        if path.is_file() and path.suffix.lower() == ".zip":
            return extract_zip_to_temp(str(path))

        if path.is_dir():
            return str(path)

        if path.is_file() and path.suffix.lower() in [".pbit", ".pdf", ".txt"]:
            return str(path)

        raise ValueError(
            f"Invalid submission path: {answer_path}\n"
            f"Path must be a directory, ZIP file, or submission file (.pbit, .pdf, .txt).\n"
            f"Found: {path.suffix} file"
        )

    def _evaluate_dax_from_path(self, working_path: str, question: str, prompt: str) -> Optional[Dict[str, Any]]:
        if question is None:
            return None

        path = Path(working_path)

        if path.is_file() and path.suffix.lower() == ".pbit":
            pbit_path = path
        else:
            pbit_file = get_file_by_type(working_path, ".pbit")
            if not pbit_file:
                return {
                    "score": 0,
                    "feedback": (
                        "Unable to evaluate submission.\n\n"
                        "The assignment includes DAX related questions, but no DAX related response(pbit file) file was found. "
                        "Please ensure your submission includes all required components and resubmit."
                    ),
                }
            pbit_path = path / pbit_file

        return self.model.evaluate(
            question=question,
            answer=analyze_pbit(str(pbit_path)),
            prompt=prompt,
        )

    def _evaluate_visual_from_path(self, working_path: str, question: str, prompt: str) -> Optional[Dict[str, Any]]:
        if question is None:
            return None

        path = Path(working_path)

        if path.is_file() and path.suffix.lower() == ".pdf":
            pdf_path = path
        else:
            pdf_file = get_file_by_type(working_path, ".pdf")
            if not pdf_file:
                return {
                    "score": 0,
                    "feedback": (
                        "Unable to evaluate submission.\n\n"
                        "The assignment includes visual type questions, but no visual type response(pdf file) file was found. "
                        "Please ensure your submission includes all required components and resubmit."
                    ),
                }
            pdf_path = path / pdf_file

        return self.model.evaluate_visual(
            question=question,
            pdf_path=str(pdf_path),
            prompt=prompt,
        )

    def _evaluate_write_from_path(self, working_path: str, question: str, prompt: str) -> Optional[Dict[str, Any]]:
        if question is None:
            return None

        path = Path(working_path)

        if path.is_file() and path.suffix.lower() == ".txt":
            txt_path = path
        else:
            txt_file = get_file_by_type(working_path, ".txt")
            if not txt_file:
                return {
                    "score": 0,
                    "feedback": (
                        "Unable to evaluate submission.\n\n"
                        "The assignment includes written type questions, but no written type response(txt file) file was found. "
                        "Please ensure your submission includes all required components and resubmit."
                    ),
                }
            txt_path = path / txt_file

        text_answer = txt_path.read_text(encoding="utf-8")

        return self.model.evaluate(
            question=question,
            answer=text_answer,
            prompt=prompt,
        )

    def evaluate_all(self, answer_path: str, questions: Dict[str, str], prompts: Dict[str, str]) -> Dict[str, Any]:
        working_path = self._prepare_answer_path(answer_path)

        results = {
            "dax": self._evaluate_dax_from_path(working_path, questions["dax"], prompts["dax"]),
            "visual": self._evaluate_visual_from_path(working_path, questions["visual"], prompts["visual"]),
            "write": self._evaluate_write_from_path(working_path, questions["write"], prompts["write"]),
        }

        scores = []
        feedback_parts = []

        for key, value in results.items():
            if value is not None:
                scores.append(value['score'])
                feedback_parts.append(
                    f"{'=' * 70}\n"
                    f"{key.upper()} EVALUATION\n"
                    f"{'=' * 70}\n"
                    f"Score: {value['score']}/100\n\n"
                    f"{value['feedback']}\n"
                )

        avg_score = sum(scores) / len(scores) if scores else 0

        summary = {
            'score': round(avg_score, 2),
            'feedback': '\n'.join(feedback_parts) if feedback_parts else "No evaluations completed."
        }

        return summary