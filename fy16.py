import csv

from clean_departments import CleanDepartments

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

with open(OUTPUT_FILE_PATH, 'wb') as f:
  keys = ['Fiscal Year', 'Fund', 'Department', 'Class ID', 'Class', 'Total']
  writer = csv.DictWriter(f, keys)
  writer.writeheader()
  writer.writerows(rows)

print('Wrote {0} rows to {1}'.format(len(rows), OUTPUT_FILE_PATH))
