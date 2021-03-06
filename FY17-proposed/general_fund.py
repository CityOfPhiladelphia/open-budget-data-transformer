from csv import writer as csv_writer

from openpyxl import load_workbook

from constants import CLASS_MATCHES
from clean_departments import CleanDepartments
from util import aggregate_similar_rows

DEPARTMENTS_FILE_PATH = './departments.yml'
INPUT_FILE_PATH = './input/Obligation History.xlsx'
OUTPUT_FILE_PATH = './output/general-fund.csv'
SHEET_NAME = 'Sheet1'

workbook = load_workbook(INPUT_FILE_PATH, read_only=True, data_only=True)
sheet = workbook.get_sheet_by_name(SHEET_NAME)
rows = list(sheet.rows)

def index_where(rows, column_index, needle):
  for row_index, row in enumerate(rows):
    if rows[column_index] and row[column_index] == needle:
      return row_index
  return -1

# Load departments and their matches
departments = CleanDepartments(DEPARTMENTS_FILE_PATH)

# Remove first 9 rows (sheet title)
rows = rows[9:]

# Only keep columns A and F
rows = [[row[0]] + [row[5]] for row in rows]

# Convert cells to strings
rows = [[cell.value for cell in row] for row in rows]

# Remove empty rows
rows = [row for row in rows if any(row)]

# Remove rows from "Total, General Fund" and after
first_row_to_remove_index = index_where(rows, 0, 'Total, General Fund')
rows = rows[:first_row_to_remove_index]

# Convert "department sections" into database-friendly rows
new_rows = []

current_dept = ''
for row in rows:
  label = row[0]
  total = row[1]

  class_match = CLASS_MATCHES.get(label)
  if class_match:
    # If it's a class, add a row to the new_rows array
    clean_dept = departments.clean(current_dept)
    new_rows.append([clean_dept, class_match['id'], class_match['name'], total])
  elif label == 'Total':
    # When 'Total' row is reached, reset current_dept
    current_dept = ''
  else:
    # Some departments span multiple lines
    if current_dept:
      current_dept = current_dept + ' ' + label.strip()
    else:
      current_dept = label.strip()

# Add year and fund columns to each row
new_rows = [['2017', 'General Fund'] + row for row in new_rows]

# Group rows by everything but total and aggregate the total (sum)
new_rows = aggregate_similar_rows(new_rows, 5)

# Sort rows for idempotency
new_rows.sort()

header = ['Fiscal Year', 'Fund', 'Department', 'Class ID', 'Class', 'Total']

with open(OUTPUT_FILE_PATH, 'wb') as f:
  writer = csv_writer(f)
  writer.writerow(header)
  writer.writerows(new_rows)

print('Wrote {0} rows to {1}'.format(len(new_rows), OUTPUT_FILE_PATH))
