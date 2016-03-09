import csv
from collections import defaultdict

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

# Group rows by everything but total and aggregate the total (sum)
grouped_rows = defaultdict(int)

for row in rows:
  key = (row['Fiscal Year'], row['Fund'], row['Department'], row['Class ID'], row['Class'])
  grouped_rows[key] += int(float(row['Total']))

# Convert the grouped dict to a list of lists
new_rows = [list(key) + [total] for key, total in grouped_rows.iteritems()]

# Sort rows for idempotency
new_rows.sort()

header = ['Fiscal Year', 'Fund', 'Department', 'Class ID', 'Class', 'Total']

with open(OUTPUT_FILE_PATH, 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(header)
  writer.writerows(new_rows)

print('Wrote {0} rows to {1}'.format(len(new_rows), OUTPUT_FILE_PATH))
