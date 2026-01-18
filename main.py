from src.models.gemini import Gemini
from pprint import pprint
from src.processors.processor import analyze_pbit
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

question = """
              **Topic:** Understanding Context in DAX & CALCULATE and Basic Filters, Variables  
        **Prerequisites:** Download DAX_Context_Practice.xlsx file.  
        
        1. What is row context? Give an example in a calculated column.  
        2. Write a measure that finds total sales  
        3. Use RELATED to fetch the Name from the Customers table into the Sales table.  
        4. What does CALCULATE(SUM(Sales[Quantity]), Sales[Category] = "Electronics") return?  
        5. Explain the difference between VAR and RETURN in DAX.  
        6. Create a calculated column in Sales called TotalPrice using row context (Quantity * UnitPrice).  
        7. Write a measure Electronics Sales using CALCULATE to sum sales only for the "Electronics" category.  
        8. Use ALL(Sales[Category]) in a measure to show total sales ignoring category filters.  
        9. Fix this error: A calculated column in Sales uses RELATED(Customers[Region]) but returns blanks.  
        10. Why does CALCULATE override existing filters?  
        11. Write a measure that returns average unitprice of products  
        12. Use VAR to store a temporary table of high-quantity sales (Quantity > 2), then count rows.  
        13. Write a measure ```% of Category Sales``` that shows each sale's contribution to its category total.  
        14. Simulate a "remove filters" button using ALL in a measure.  
        15. Troubleshoot: A CALCULATE measure ignores a slicer. What’s the likely cause?
        
        ```Download DAX_Context_Practice```
        | SaleID | ProductID | CustomerID | Quantity | UnitPrice | Category    |
        |--------|-----------|------------|----------|-----------|-------------|
        | 1      | P1        | C1         | 2        | 100       | Electronics |
        | 2      | P2        | C2         | 1        | 50        | Clothing    |
        | 3      | P1        | C1         | 3        | 100       | Electronics |
"""

answer = analyze_pbit("tests/files/lesson-9/*.pbit")

prompt = """
    Please review the follwing power bi report here is what is included in the report
"""

tutor = Gemini(api_key=API_KEY, model_name="gemini-3-pro-preview")

result = tutor.evaluate(
    question=question,
    answer=answer,
    prompt=prompt,
)

pprint(result)