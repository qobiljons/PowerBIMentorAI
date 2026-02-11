PowerBIMentor
=============

A Python package for extracting metadata from Power BI `.pbit` templates and evaluating them using AI models like Google Gemini.

## Features

- 📊 **PBIT Processing**: Extract and parse Power BI template metadata (DataModelSchema)
- 🤖 **AI Evaluation**: Evaluate DAX formulas, visualizations, and written answers using Google Gemini
- 📝 **Detailed Reports**: Generate comprehensive grading reports from Power BI models
- 📦 **ZIP Support**: Automatically handles ZIP file submissions - no manual extraction needed
- 🔧 **Easy Integration**: Simple API for evaluating student assignments and projects

## Installation

### From Source

```bash
git clone https://github.com/yourusername/PowerBIMentor.git
cd PowerBIMentor
pip install -e .
```

### Using pip (when published)

```bash
pip install PowerBIMentor
```

## Quick Start

```python
from PowerBIMentor import PowerBIMentor

# Initialize with your Gemini API key
mentor = PowerBIMentor(api_key="your-api-key")

# Evaluate a full submission (DAX + visuals + written)
# Works with directories, ZIP files, or single files (.pbit/.pdf/.txt)
questions = {
    "dax": "Create measures for total sales and profit margin",
    "visual": "Build a sales dashboard with KPIs and trends",
    "write": "Explain your design choices and insights",
}

prompts = {
    "dax": "Evaluate DAX correctness and best practices",
    "visual": "Evaluate layout, clarity, and chart selection",
    "write": "Evaluate clarity and reasoning",
}

result = mentor.evaluate_all(
    answer_path="path/to/submission/",  # or "submission.zip"
    questions=questions,
    prompts=prompts,
)

print(f"Score: {result['score']}/100")
print(f"Feedback:\n{result['feedback']}")
```

## Package Structure

```
PowerBIMentor/
├── __init__.py           # Main package entry point
├── core.py               # PowerBIMentor class with evaluation methods
├── models/               # AI model wrappers
│   ├── __init__.py
│   ├── model.py          # Abstract base model
│   └── gemini.py         # Google Gemini implementation
└── utils/                # Utility functions
    ├── __init__.py
    ├── processor.py      # PBIT parsing and report generation
    ├── checker.py        # File discovery helpers
    └── extractor.py      # ZIP extraction utilities
```

## Core Components

### PowerBIMentor Class

The main class provides a single evaluation method:

- **`evaluate_all(answer_path, questions, prompts)`**: Evaluates DAX, visuals, and written answers together and returns an overall score and combined feedback

### PBIT Processor

`PowerBIMentor.utils.processor` provides functions for processing Power BI templates:

#### `pbit_to_json(pbit_path)`
Extracts and parses the DataModelSchema from a `.pbit` file:
- Handles UTF-16 encoding and quote normalization
- Returns the parsed JSON model structure

#### `extract_grading_info(model)`
Extracts key elements for grading:
- Tables, columns, and measures (excluding hidden/private items)
- Relationships (excluding LocalDateTable)
- Hierarchies (excluding template hierarchies)
- Data source information from M code

#### `generate_grading_report(grading_info)`
Formats extracted information into a readable text report

#### `analyze_pbit(pbit_path)`
Convenience function that chains all three steps above

### AI Models

#### Gemini Model
`PowerBIMentor.models.gemini.Gemini`

```python
from PowerBIMentor.models import Gemini

model = Gemini(api_key="your-api-key", model_name="gemini-2.0-flash-exp")

# Evaluate text-based answers
result = model.evaluate(
    question="What is DAX?",
    answer="DAX stands for Data Analysis Expressions...",
    prompt="Evaluate for accuracy and completeness"
)

# Evaluate PDF visualizations
result = model.evaluate_visual(
    question="Review the dashboard design",
    prompt="Evaluate layout, clarity, and best practices",
    pdf_path="dashboard.pdf"
)
```

**Response Format:**
```json
{
  "score": 85,
  "feedback": "Strong implementation with minor issues..."
}
```

## Configuration

### API Key Setup

Create a `.env` file in your project root:

```env
API_KEY=your_gemini_api_key_here
```

Load it in your code:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

## Detailed Usage Examples

### 1. Analyze a PBIT File

```python
from PowerBIMentor.utils import analyze_pbit

# Generate a detailed report from a Power BI template
report = analyze_pbit("path/to/file.pbit")
print(report)
```

**Sample Output:**
```
Model: Sales Analysis
Compatibility Level: 1550

Data Source:
  Type: File
  Path: C:\Data\Sales.xlsx

Tables:
  - Sales
    Columns:
      • Date (type=dateTime, summarize_by=none, calculated=False)
      • Product (type=string, summarize_by=none, calculated=False)
      • Amount (type=double, summarize_by=sum, calculated=False)
    Measures:
      • Total Sales
      • Profit Margin

Measures (details):
  - Total Sales (table: Sales)
      SUM(Sales[Amount])

  - Profit Margin (table: Sales)
      DIVIDE([Total Profit], [Total Sales], 0)

Relationships:
  - Sales[Date] -> Calendar[Date] (standard)

Summary:
  - main_table: Sales
  - total_columns: 3
  - total_measures: 2
  - total_relationships: 1
  - has_time_intelligence: False
```

### 2. Complete Evaluation Pipeline

```python
from PowerBIMentor import PowerBIMentor

mentor = PowerBIMentor(api_key="your-api-key")

# Define questions and prompts for each evaluation type
questions = {
    "dax": "Create measures for total sales and YoY growth",
    "visual": "Create a sales dashboard with KPIs and trends",
    "write": "Explain your dashboard design choices"
}

prompts = {
    "dax": "Evaluate DAX correctness, best practices, and time intelligence",
    "visual": "Evaluate layout, chart selection, and design principles",
    "write": "Evaluate clarity, justification, and understanding"
}

# Evaluate all aspects
result = mentor.evaluate_all(
    answer_path="path/to/student/submission/",
    questions=questions,
    prompts=prompts
)

print(f"Overall Score: {result['score']}/100")
print(f"Feedback:\n{result['feedback']}")
```

### 3. Custom Model Usage

```python
from PowerBIMentor.models import Gemini
from PowerBIMentor.utils import analyze_pbit

# Initialize with specific model
model = Gemini(api_key="your-api-key", model_name="gemini-2.0-flash-exp")

# Get PBIT analysis
analysis = analyze_pbit("assignment.pbit")

# Evaluate with custom prompt
result = model.evaluate(
    question="Implement sales analysis with time intelligence",
    answer=analysis,
    prompt="""
    Evaluate the implementation considering:
    1. Correct use of DAX functions
    2. Time intelligence measures
    3. Proper relationships
    4. Performance optimization
    """
)

print(f"Score: {result['score']}/100")
print(f"Feedback:\n{result['feedback']}")
```

## Examples

The `examples/` directory contains comprehensive usage examples:

- **`quick_start.py`**: Simplest introduction (start here!)
- **`basic_usage.py`**: Comprehensive guide to core features
- **`advanced_usage.py`**: Advanced features and batch processing
- **`classroom_grading.py`**: Practical example for grading student assignments

See [examples/README.md](examples/README.md) for detailed documentation.

```bash
# Run the quick start example
python examples/quick_start.py

# Run comprehensive examples
python examples/basic_usage.py
```

## Development

### Running Tests

```bash
# Run processor tests
python tests/processors/processor.py

# Run model tests
python tests/models/gemini.py

# Run integration tests
python tests/test.py
```

### Project Dependencies

Core:
- `google-genai>=1.0.0` - Google Gemini API client
- `python-dotenv>=1.0.0` - Environment variable management

Optional:
- `google-cloud-aiplatform>=1.0.0` - For Vertex AI support

## Requirements

- Python 3.9 or higher
- Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details
