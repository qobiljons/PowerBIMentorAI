from src.models.vertex import VertexGemini

PROJECT_ID = "master-haven-458406-v1"

question = "What is 2 + 2?"
answer = "2 + 2 equals 4."
prompt = "Evaluate the answer for correctness and clarity."

tutor = VertexGemini(
    project_id=PROJECT_ID,
    location="us-central1",
    model_name="gemini-2.5-pro",
)

tutor.display_content(question, answer, prompt)

result = tutor.evaluate(
    question=question,
    answer=answer,
    prompt=prompt,
)

print("\n=== MODEL OUTPUT ===")
print(result)