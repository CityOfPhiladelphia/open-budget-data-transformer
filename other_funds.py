from csv import writer
import re

from yaml import load
from xlrd import open_workbook
from titlecase import titlecase

from constants import FUNDS, CLASS_NAMES

DEPARTMENTS_FILE_PATH = './departments.yml'
OUTPUT_FILE_NAME = './output/other-funds.csv'

def float_or_zero(str):
  if str: return float(str)
  else: return 0

def index_where_starts_with(rows, column_index, needle):
  for row_index, row in enumerate(rows):
    if rows[column_index] and row[column_index].startswith(needle):
      return row_index
  return -1

def construct_dept_rows(fund, dept, row):
  dept_rows = []

  if row[u'CLASS 100'] or row[u'PENSIONS'] or row[u'OTHER FB']:
    total_class_100 = float_or_zero(row[u'CLASS 100']) + float_or_zero(row[u'PENSIONS']) + float_or_zero(row[u'OTHER FB'])
    dept_rows.append(['2017', fund, dept, 100, CLASS_NAMES['100'], total_class_100])
  if row[u'CLASS 300'] or row[u'CLASS 400']:
    total_class_300 = float_or_zero(row[u'CLASS 300']) + float_or_zero(row[u'CLASS 400'])
    dept_rows.append(['2017', fund, dept, 300, CLASS_NAMES['300'], total_class_300])

  for key in ['200', '500', '700', '800', '900']:
    if row.get(u'CLASS ' + key):
      dept_rows.append(['2017', fund, dept, key, CLASS_NAMES[key], row[u'CLASS ' + key]])

  return dept_rows

def cleanup_department(dept):
  dashes_replaced = re.sub(r'(?! )-(?! )', ' - ', dept)
  title_cased = titlecase(dashes_replaced)
  match = dept_matches.get(title_cased)
  if not match: raise KeyError('No match found for {0}'.format(title_cased))
  return match

def load_department_matches(file_path):
  dept_matches = {}

  with open(file_path, 'rb') as file:
    rows = load(file)

    for row in rows:
      if isinstance(row, dict):
        # If it's a dict, add a match for the key, and for each of the values
        for name, variations in row.iteritems(): # only one of these
          dept_matches[name] = name
          for variation in variations:
            dept_matches[variation] = name
      else:
        # Otherwise it's just a string; add a match for it
        dept_matches[row] = row

  return dept_matches

dept_matches = load_department_matches(DEPARTMENTS_FILE_PATH)

new_rows = [['Fiscal Year', 'Fund', 'Department', 'Class ID', 'Class', 'Total']]

for fund in FUNDS:
  workbook = open_workbook(fund['input'])
  sheet = workbook.sheet_by_name(fund['sheet'])

  # Convert rows to list
  rows = []
  for row_index in range(sheet.nrows):
    rows.append(sheet.row_values(row_index))

  # Remove unneeded rows at top
  rows = rows[4:]

  # Only keep columns A and C through K
  rows = [[row[0]] + row[2:12] for row in rows]

  # Remove empty rows
  rows = [row for row in rows if any(row)]
  
  # Remove rows from "TOTAL XX FUND" and after
  total_row_index = index_where_starts_with(rows, 0, 'TOTAL')
  rows = rows[:total_row_index]

  # Convert list of lists to list of dicts
  keys = rows[0]
  rows = rows[1:]
  rows = [dict(zip(keys, row)) for row in rows]

  # Convert "department sections" to individual department rows using FY17 amount
  fund_rows = []
  current_dept = ''
  for row in rows:
    label = row[u'Department']

    if label.startswith('FY17'):
      new_rows = new_rows + construct_dept_rows(fund['name'], current_dept, row)
    elif not label.startswith('FY16') and not label.startswith('INCREASE') and not label.startswith('TOTAL'):
      current_dept = cleanup_department(label)

with open(OUTPUT_FILE_NAME, 'wb') as f:
  writer(f).writerows(new_rows)

print('Wrote {0} rows to {1}'.format(len(new_rows), OUTPUT_FILE_NAME))
