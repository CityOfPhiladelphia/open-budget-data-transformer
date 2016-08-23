import csv

INPUT_FILE_PATHS = [
  './output/general-fund.csv',
  './output/other-funds.csv',
]
OUTPUT_FILE_PATH = './output/FY2017-proposed.csv'

header = []
combined_rows = []

for input_file in INPUT_FILE_PATHS:
  with open(input_file, 'rb') as file:
    rows = list(csv.reader(file))
    if not header: header = rows[0]
    combined_rows = combined_rows + rows[1:]

# Sort rows for idempotency
combined_rows.sort()

with open(OUTPUT_FILE_PATH, 'wb') as file:
  writer = csv.writer(file)
  writer.writerow(header)
  writer.writerows(combined_rows)

print('Wrote {0} rows to {1}'.format(len(combined_rows), OUTPUT_FILE_PATH))
