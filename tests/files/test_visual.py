from pprint import pprint
from src.models.gemini import Gemini
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

tutor = Gemini(api_key=API_KEY, model_name="gemini-3-pro-preview")
question = """
      ## Lesson 8  
            **Topic:** Introduction to DAX Basics & Calculated Columns vs. Measures  
            **Prerequisites:** Download DAX_Practice_Data.xlsx file  
            1. What does DAX stand for?  
            2. Write a DAX formula to sum the Sales column.  
            3. What is the difference between a calculated column and a measure?  
            4. Use the DIVIDE function to calculate Profit Margin (Profit/Sales).  
            5. What does COUNTROWS() do in DAX?  
            6. Create a measure: Total Profit that subtracts total cost from total sales  
            7. Write a measure to calculate Average Sales per Product.  
            8. Use IF() to tag products as "High Profit" if Profit > 1000.  
            9. What is a circular dependency error in a calculated column?  
            10. Explain row context vs. filter context.  
            11. Write a measure to calculate YTD Sales using TOTALYTD().  
            12. Create a dynamic measure that switches between Sales, Profit, and Margin.  
            13. Optimize a slow DAX measure using variables (VAR).  
            14. Use CALCULATE() to override a filter  
            15. Write a measure that returns the highest sales amount  

```DAX_Practice_Data```
| ProductID | Sales | Cost | Date      |
|-----------|-------|------|-----------|
| 1         | 6000  | 4000 | 1/1/2023  |
| 2         | 3000  | 2000 | 1/2/2023  |
| 3         | 2000  | 1500 | 1/3/2023  |
"""

result = tutor.evaluate_visual(
    question=question,
    prompt="You are a strict Power BI instructor grading student understanding.",
    pdf_path="./lesson-8/Lesson - 8.pdf",
)

pprint(result)
