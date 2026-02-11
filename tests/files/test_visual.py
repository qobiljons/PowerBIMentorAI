import sys
from pathlib import Path
from pprint import pprint
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from PowerBIMentor.models.gemini import Gemini

load_dotenv()

API_KEY = os.getenv("API_KEY")

tutor = Gemini(api_key=API_KEY, model_name="gemini-3-pro-preview")
question = """
        Review the report and mark it 
"""

result = tutor.evaluate_visual(
    question=question,
    prompt="",
    pdf_path="tests/files/lesson-9/dashboard.pdf",
)

pprint(result)
