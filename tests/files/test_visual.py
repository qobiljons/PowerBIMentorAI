from pprint import pprint
from src.models.gemini import Gemini
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

tutor = Gemini(api_key=API_KEY, model_name="gemini-3-pro-preview")
question = """
        Review the report and mark it 
"""

result = tutor.evaluate_visual(
    question=question,
    prompt="",
    pdf_path="dashboard.pdf",
)

pprint(result)
