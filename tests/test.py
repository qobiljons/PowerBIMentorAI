from pprint import pprint
from PowerBIMentor import PowerBIMentor

questions = {
    "dax": "Create measures for sales analysis with time intelligence",
    "visual": "Visual",
    "write": "Explain your design choices and DAX implementation strategy"
}

prompts = {
    "dax": "Evaluate DAX correctness, best practices, and time intelligence implementation make sure to give short answer about 30-40 words",
    "visual": "Evaluate layout, chart selection, and dashboard design principles make sure to give short answer about 30-40 words",
    "write": "Evaluate clarity of explanation and understanding of concepts make sure to give short answer about 30-40 words",
}

mentor = PowerBIMentor(api_key="", model_name="gemini-2.5-flash-lite")

results = mentor.evaluate_all(
    answer_path="files/lesson-9",
    questions=questions,
    prompts=prompts
)

pprint(results)