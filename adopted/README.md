# adopted
Cleans the adopted budget, which comes from a report run in the financial data
warehouse and is exported as a CSV file. The adopted budget is typically
available around July each year and is much simpler to process than the proposed
budget.

The first time this script was used was for the FY17 adopted budget. The
processing for prior budgets was done using a Node.js script. As a result, some
of the string cleanup is slightly different (ex. title case logic) and can cause
inconsistencies when comparing between FY16-and-prior and FY17-and-later.

Usage
1. Activate virtual environment using `venv/bin/activate`
2. Install dependencies using `pip install -r requirements.txt`
3. Execute cleanup using the below command

```bash
cat input/<filename>.csv | python clean_adopted.py > output/FY17-adopted.csv
```
