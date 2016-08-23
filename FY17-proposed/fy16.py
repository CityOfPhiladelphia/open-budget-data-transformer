import csv

from clean_departments import CleanDepartments
from util import aggregate_similar_rows

INPUT_FILE_PATH = './input/FY2016-proposed.csv'
OUTPUT_FILE_PATH = './output/FY2016-proposed.csv'
DEPARTMENTS_FILE_PATH = './departments.yml'

# Load departments and their matches
departments = CleanDepartments(DEPARTMENTS_FILE_PATH)

with open(INPUT_FILE_PATH, 'rb') as file:
  rows = list(csv.DictReader(file))

for row in rows:
  # Cleanup department
  row['Department'] = departments.clean(row['Department'])

  # Rename classes 300 and 400
  if row['Class ID'] in ['300', '400']:
    row['Class ID'] = '300'
    row['Class'] = 'Materials, Supplies & Equipment'

# Convert list of dicts to list of lists
list_rows = [[row['Fiscal Year'], row['Fund'], row['Department'], row['Class ID'], row['Class'], row['Total']] for row in rows]

# Group rows by everything but total and aggregate the total (sum)
new_rows = aggregate_similar_rows(list_rows, 5)

# Sort rows for idempotency
new_rows.sort()

header = ['Fiscal Year', 'Fund', 'Department', 'Class ID', 'Class', 'Total']

with open(OUTPUT_FILE_PATH, 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(header)
  writer.writerows(new_rows)

print('Wrote {0} rows to {1}'.format(len(new_rows), OUTPUT_FILE_PATH))
