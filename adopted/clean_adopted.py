import csv
from sys import stdin, stdout
from re import sub

from titlecase import titlecase

field_map = {
  'fiscal_year': 'FY',
  'fund': 'Fund Title',
  'department': 'Department Title',
  'class_id': 'Char',
  'class': 'Character Title',
  'subclass_id': 'Sub-obj',
  'subclass': 'Sub-object Title',
  'total': 'Original Appn Balance',
}

header = ['fiscal_year', 'fund', 'department', 'class_id',
          'class', 'subclass_id', 'subclass', 'total']

def remove_codes (input):
  return sub(r'\d\d+', '', input)

def clean_title (input):
  return titlecase(remove_codes(input).strip())

def clean_fiscal_year (row):
  return row[field_map['fiscal_year']]

def clean_fund (row):
  fund = row[field_map['fund']]
  return clean_title(fund.replace('FD', 'FUND'))

def clean_department (row):
  department = row[field_map['department']]
  subclass_id = int(row[field_map['subclass_id']])
  fund = row[field_map['fund']]

  # Classes 186 through 198 should be in a distinct department
  if (subclass_id >= 186 and subclass_id <= 198 and 'GRANTS REVENUE' not in fund):
    return 'Finance - Employee Benefits'
  elif ('OFFICE OF TECHNOLOGY' in department):
    return 'Office of Innovation & Technology'
  else:
    return clean_title(department)

  return department

def clean_class_id (row):
  return row[field_map['class_id']]

def clean_class (row):
  class_id = int(row[field_map['class_id']])
  _class = row[field_map['class']]
  if (class_id == 5):
    return 'Contributions, Indemnities, Refunds, Taxes'
  else:
    return clean_title(_class)

def clean_subclass_id (row):
  return row[field_map['subclass_id']]

def clean_subclass (row):
  subclass_id = int(row[field_map['subclass_id']])
  subclass = row[field_map['subclass']]

  if (subclass_id == 191):
    return 'Pension'
  elif (subclass_id == 192):
    return 'FICA Taxes'
  else:
    return clean_title(subclass)

def clean_total (row):
  return int(float(row[field_map['total']]))

rows = csv.DictReader(stdin)
writer = csv.DictWriter(stdout, fieldnames=header)
writer.writeheader()
for row in rows:
  clean_row = {
    'fiscal_year': clean_fiscal_year(row),
    'fund': clean_fund(row),
    'department': clean_department(row),
    'class_id': clean_class_id(row),
    'class': clean_class(row),
    'subclass_id': clean_subclass_id(row),
    'subclass': clean_subclass(row),
    'total': clean_total(row),
  }
  writer.writerow(clean_row)
