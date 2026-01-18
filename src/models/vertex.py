from vertexai import init
from vertexai.generative_models import GenerativeModel

from src.models.model import Model
from src.models.model import build_content


class VertexGemini(Model):
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "gemini-2.5-pro",
    ):
        super().__init__()
        init(project=project_id, location=location)
        self.model = GenerativeModel(model_name)

    def evaluate(self, question: str, answer: str, prompt: str = "") -> str:
        contents = build_content(question, answer, prompt)
        response = self.model.generate_content(contents)
        return response.text

    def display_content(self, question: str, answer: str, prompt: str = "") -> None:
        print(build_content(question, answer, prompt))