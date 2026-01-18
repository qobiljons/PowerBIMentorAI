import json
from typing import Any, Dict
from google import genai
from src.models.model import Model, build_content

class Gemini(Model):
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        super().__init__()
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def evaluate(self, question: str, answer: str, prompt: str) -> Dict[str, Any]:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=build_content(question, answer, prompt),
        )

        text = (response.text or "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Model did not return valid JSON.\nRaw output:\n{text}") from e

    # def evaluate_visual(self, question: str, answer: str, prompt: str) -> Dict[str, Any]:
    #
    #     response = self.client.models.generate_content(
    #         model=self.model_name,
    #         contents=build_content(question, answer, prompt),
    #     )
    #
    #     text = (response.text or "").strip()
    #
    #     try:
    #         return json.loads(text)
    #     except json.JSONDecodeError as e:
    #         raise ValueError(f"Model did not return valid JSON.\nRaw output:\n{text}") from e