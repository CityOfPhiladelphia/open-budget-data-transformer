# Validator
Automates spotchecking by comparing a YAML file of expected values
to the processed CSV files and `data.json` file.

## usage
To validate the `data.json` file:
```bash
validate.py json data.json tests/FY18-adopted-tests.yml 2018
```

To validate the processed `.csv` files:
```bash
validate.py csv FY18-adopted.csv tests/FY18-adopted-tests.yml
```

## test format
```yaml
- fund: General Operating Fund
  department: City Council
  class: Personal Services
  total: 100000

- fund: General Operating Fund
  department: Mayor's Office-Labor Relations
  class: Purchase of Services
  total: 1500
```

## note
- Proposed budgets combine the `Materials and Supplies` and `Equipment`
classes into one `Materials, Supplies and Equipment` class. Adopted
budgets have them separate.
