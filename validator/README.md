# Validator
Automates spotchecking by comparing a YAML file of expected lines
to the processed data.

## usage
```bash
python validator.py FY18-adopted.csv FY18-adopted-tests.yml
```

## test format
```yaml
- fund: General Operating Fund
  department: City Council
  class: Personal Services
  subclass: Salary Control
  total: 100000

- fund: General Operating Fund
  department: Mayor's Office-Labor Relations
  class: Purchase of Services
  subclass: Transportation
  total: 1500
```

## note
- Proposed budgets do not have subclasses, so the tests should
exclude the `subclass` line, and reflect the total for the overall
`class`.
- Proposed budgets combine the `Materials and Supplies` and `Equipment`
classes into one `Materials, Supplies and Equipment` class. Adopted
budgets have them separate.
