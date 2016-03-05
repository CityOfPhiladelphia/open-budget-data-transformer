# Open Budget 2017 Parser 
Parses the MS Excel spreadsheets the Budget Office uses into a CSV format with one record for 
every year-fund-department-class for use in the
[open-budget](https://github.com/cityofphiladelphia/open-budget) app.

# Installation
1. Clone this repo
2. Optionally, create a virtual environment using `virtualenv venv`
and activate it via `. venv/bin/activate`
3. Install dependencies via `pip install -r requirements.txt`

# Usage
```sh
python general_fund.py
python other_funds.py
```
