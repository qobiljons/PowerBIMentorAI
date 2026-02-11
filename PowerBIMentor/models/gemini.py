import json
from pathlib import Path
from typing import Any, Dict, Union
from google import genai
from google.genai import types
from .model import Model, build_content, build_visual_content



class Gemini(Model):
    """Google Gemini model wrapper for evaluations.

    Uses the Google Gemini API to evaluate student submissions with
    structured JSON responses containing scores and feedback.

    Attributes:
        client: Google Gemini API client
        model_name: Name of the Gemini model to use
        response_schema: JSON schema for structured responses
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize the Gemini model.

        Args:
            api_key: Your Google Gemini API key
            model_name: Model to use (default: gemini-2.0-flash-exp)
        """
        super().__init__()
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

        self.response_schema = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "score": {
                        "type": "number",
                        "description": "The numerical score for the evaluation"
                    },
                    "feedback": {
                        "type": "string",
                        "description": "Detailed feedback explaining the score"
                    }
                },
                "required": ["score", "feedback"]
            }
        )

    def evaluate(self, question: str, answer: str, prompt: str) -> Dict[str, Any]:
        """Evaluate a text-based answer.

        Args:
            question: The assignment question
            answer: The student's answer
            prompt: Evaluation criteria and instructions

        Returns:
            Dictionary with 'score' (int, 0-100) and 'feedback' (str)

        Raises:
            ValueError: If the model doesn't return valid JSON or missing fields
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=build_content(question, answer, prompt),
            config=self.response_schema,
        )

        text = (response.text or "").strip()

        try:
            result = json.loads(text)

            if "score" not in result or "feedback" not in result:
                raise ValueError(f"Missing required fields (score, feedback) in response: {result}")
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Model did not return valid JSON.\nRaw output:\n{text}") from e

    def evaluate_visual(
            self,
            question: str,
            prompt: str,
            pdf_path: Union[str, Path],
    ) -> Dict[str, Any]:
        """Evaluate a PDF document (e.g., dashboard visualizations).

        Args:
            question: The assignment question
            prompt: Evaluation criteria and instructions
            pdf_path: Path to the PDF file to evaluate

        Returns:
            Dictionary with 'score' (int, 0-100) and 'feedback' (str)

        Raises:
            ValueError: If the PDF path is invalid or model returns invalid JSON
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"Invalid PDF path: {pdf_path}")

        pdf_bytes = pdf_path.read_bytes()

        contents = [
            {
                "text": build_visual_content(question, prompt)
            },
            {
                "inline_data": {
                    "mime_type": "application/pdf",
                    "data": pdf_bytes,
                }
            },
        ]

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=self.response_schema,
        )
        text = (response.text or "").strip()

        try:
            result = json.loads(text)

            if "score" not in result or "feedback" not in result:
                raise ValueError(f"Missing required fields (score, feedback) in response: {result}")
            return result
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Model did not return valid JSON.\nRaw output:\n{text}"
            ) from e