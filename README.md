PowerBIMenor
============

Purpose
-------
PowerBIMenor extracts model metadata from Power BI `.pbit` templates and can send that metadata to Gemini-based evaluators. The current codebase provides:

- A PBIT processor that reads `DataModelSchema` and produces a grading report.
- Model wrappers for Google Gemini (API key) and Vertex AI Gemini (project-based).
- Test scripts showing how to run the processor and model evaluations.

There is also a legacy end-to-end evaluator in `old.py` that handles ZIP/PDF inputs and uses the REST Gemini API.

Project Layout
--------------
- `src/processors/processor.py`: Core PBIT parser and grading report generator.
- `src/models/model.py`: Abstract model interface + prompt builder.
- `src/models/gemini.py`: Gemini API key client wrapper (JSON response expected).
- `src/models/vertex.py`: Vertex AI Gemini wrapper (plain text response).
- `main.py`: Simple example of calling the Gemini wrapper.
- `old.py`: Legacy full pipeline (PBIT + PDF visual evaluation).
- `tests/`: Example scripts and sample PBIT/PDF files.

What the Processor Does
-----------------------
`src/processors/processor.py` implements:

1) `pbit_to_json(pbit_path)`
   - Copies `.pbit` to a temp zip, extracts it, and loads `DataModelSchema` (or `DataModelSchema.txt`).
   - Decodes the schema as UTF-16 and normalizes curly quotes.
   - Returns the parsed JSON model.

2) `extract_grading_info(model)`
   - Builds a structured summary:
     - Tables, columns, and measures (hidden/private tables are skipped).
     - Relationships (ignores `LocalDateTable`).
     - Hierarchies (skips template hierarchies).
     - Data source path when M code uses `File.Contents("...")`.
   - Adds a summary (counts, main table, time-intelligence hint).

3) `generate_grading_report(grading_info)`
   - Formats the extracted info as a readable text report.

4) `analyze_pbit(pbit_path)`
   - Convenience wrapper: `pbit_to_json` → `extract_grading_info` → `generate_grading_report`.

Model Evaluators
----------------
`src/models/model.py`
- `build_content(question, answer, prompt)` formats the prompt and demands JSON:
  - `{"score": number (0-100), "feedback": string}`
- `Model` defines the abstract `evaluate(...)` method.

`src/models/gemini.py`
- `Gemini(api_key, model_name="gemini-2.5-flash")`
- `evaluate(question, answer, prompt)`:
  - Calls the Gemini API via `google.genai`.
  - Parses JSON from the response text.
  - Raises `ValueError` if the model does not return valid JSON.

`src/models/vertex.py`
- `VertexGemini(project_id, location="us-central1", model_name="gemini-2.5-pro")`
- `evaluate(question, answer, prompt)`:
  - Calls Vertex AI and returns raw text.
  - Does not parse JSON.

Legacy Pipeline (old.py)
------------------------
`old.py` contains a full evaluator that:
- Accepts `.pbit`, `.pdf`, or `.zip` inputs.
- Extracts the data model, scores DAX content via REST Gemini API.
- Converts PDF pages to images and scores visuals.
- Returns a combined score and feedback.

This file is self-contained and does not use the newer `src/processors/processor.py` output format.

Requirements
------------
No dependency file is provided. The code imports these third-party packages:

- `google-genai` (for `src/models/gemini.py`)
- `vertexai` (for `src/models/vertex.py`)
- `requests`, `python-dotenv`, `pdf2image`, `Pillow`, `tenacity` (used in `old.py`)

The repository includes `.pyc` files built with Python 3.14 (`cpython-314`). No minimum version is specified in code.

Configuration
-------------
- Gemini API key:
  - `src/models/gemini.py` expects `api_key` passed directly.
  - `old.py` loads `GEMINI_API_KEY` from environment or `.env`.
- Vertex AI:
  - `src/models/vertex.py` requires a `project_id` and valid Vertex AI credentials
    (Application Default Credentials).

Usage Examples
--------------
Analyze a PBIT file and generate a report:

```python
from src.processors.processor import analyze_pbit

report = analyze_pbit("tests/files/lesson-8/Lesson - 8.pbit")
print(report)
```

Score a response using Gemini (JSON response expected):

```python
from src.models.gemini import Gemini

tutor = Gemini(api_key="YOUR_API_KEY", model_name="gemini-3-flash-preview")
result = tutor.evaluate(
    question="What is 2 + 2?",
    answer="It is 4.",
    prompt="Regarding the question, mark the answer from 0 to 100",
)
print(result)  # {"score": ..., "feedback": "..."}
```

Use Vertex AI Gemini (plain text response):

```python
from src.models.vertex import VertexGemini

tutor = VertexGemini(project_id="your-gcp-project-id")
text = tutor.evaluate(
    question="What is 2 + 2?",
    answer="It is 4.",
    prompt="Evaluate the answer for correctness and clarity.",
)
print(text)
```

Tests / Example Scripts
-----------------------
These are plain Python scripts, not a pytest suite:

```bash
python tests/processors/processor.py
python tests/models/gemini.py
python tests/models/vertex.py
```

Each script hardcodes a sample file path and/or API key; edit them before running.
