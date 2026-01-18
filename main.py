from src.Models.model import Gemini

API_KEY = ""

question = "What is 2 + 2."
answer = "it is 4"
prompt = "Regarding the question, mark the answer from 0 to 100"

tutor = Gemini(
    api_key=API_KEY,
    model_name="gemini-3-flash-preview"
)

result = tutor.evaluate(
    question=question,
    answer=answer,
    prompt=prompt
)

print(result)