from src.models.gemini import Gemini
from pprint import pprint
from src.processors.processor import analyze_pbit
from src.dir.checker import get_file_by_type
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

question = {
    "write": "In 2–3 sentences, explain what a measure is in Power BI. What is the difference between a calculated column and a measure? When would you prefer a star schema over a flat table? (Give 1 reason)",
    "dax": "Write a measure for Total Sales = SUM(Sales[Amount]). Write a measure for Total Orders = COUNTROWS(Sales). Write a measure for Average Sales per Order = DIVIDE([Total Sales], [Total Orders]). Write a measure to calculate Sales YTD using a Date table.",
    "visual": "Which 3 visuals would you use to show KPI, trend over time, and category comparison? Name 2 best practices for slicers or filters placement in a report. How would you design the first page to be executive-friendly? What makes a report readable and not cluttered? List 2 points."
}


answer_path = "files/lesson-9/"

prompt = {
    "write": "Check if the written answer is correct, clear, and conceptually accurate.",
    "dax": "Check if the DAX is syntactically correct, logically correct, and follows best practices.",
    "visual": "Check if the report visuals are appropriate, clean, and well designed."
}

tutor = Gemini(api_key=API_KEY, model_name="gemini-3-flash-preview")


pbit_file = get_file_by_type(answer_path, ".pbit")
if pbit_file:
    result = tutor.evaluate(
        question=question["dax"][0],
        answer=analyze_pbit(f"{answer_path}/{pbit_file}"),
        prompt=prompt["dax"]
    )
    pprint(result)


pdf_file = get_file_by_type(answer_path, ".pdf")
if pdf_file:
    pdf_result = tutor.evaluate_visual(
        question=question["visual"][0],
        pdf_path=f"{answer_path}/{pdf_file}",
        prompt=prompt["visual"]
    )
    pprint(pdf_result)


txt_file = get_file_by_type(answer_path, ".txt")
print(question["write"])
print(txt_file)
if txt_file:
    with open(f"{answer_path}/{txt_file}", "r", encoding="utf-8") as f:
        text_answer = f.read()

    txt_result = tutor.evaluate(
        question=question["write"],
        answer=text_answer,
        prompt=prompt["write"]
    )
    pprint(txt_result)
