from openpyxl import load_workbook

FILE_NAME = './input/Obligation History.xlsx'
SHEET_NAME = 'Sheet1'

workbook = load_workbook(FILE_NAME, read_only=True, data_only=True)
sheet = workbook.get_sheet_by_name(SHEET_NAME)
rows = list(sheet.rows)

def index_where(rows, column_index, needle):
  for row_index, row in enumerate(rows):
    if rows[column_index] and row[column_index] == needle:
      return row_index
  return -1

# def concat_rows(rows):
#   return [' '.join(filter(None, column)) for column in zip(*rows)]

# Convert cells to strings
rows = [[cell.value for cell in row] for row in rows]

# Remove first 9 rows (sheet title)
rows = rows[9:]

# Remove column G and after
# rows = [row[:6] for row in rows]

# Only keep columns A and F
rows = [[row[0]] + [row[5]] for row in rows]

# Remove empty rows
rows = [row for row in rows if any(row)]# and row[0] != 'Total']

# Remove rows from "Total, General Fund" and after
first_row_to_remove_index = index_where(rows, 0, 'Total, General Fund')
rows = rows[:first_row_to_remove_index]

# Concatenate first 4 rows
# header_row = concat_rows(rows[:4])
# rows = [header_row] + rows[4:]

for row in rows:
  # print [cell.value for cell in row]
  print row
  # for cell in row:
  #   print(cell.value)
