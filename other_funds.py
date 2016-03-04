from csv import writer

from xlrd import open_workbook

FUNDS = [
  {
    'input': './input/04-CountyLiq.XLS',
    'output': './output/county-liquid.csv',
    'sheet': 'A',
  },
  {
    'input': './input/05-SpecGas.XLS',
    'output': './output/spec-gas.csv',
    'sheet': 'A',
  },
  {
    'input': './input/06-HealthCh.XLS',
    'output': './output/health-ch.csv',
    'sheet': 'A',
  },
  {
    'input': './input/07-Hotel.XLS',
    'output': './output/hotel.csv',
    'sheet': 'A',
  },
  {
    'input': './input/08-Grants.XLS',
    'output': './output/grants.csv',
    'sheet': 'A',
  },
  {
    'input': './input/09-Aviation.XLS',
    'output': './output/aviation.csv',
    'sheet': 'A',
  },
  {
    'input': './input/10-CommDev.XLS',
    'output': './output/comm-dev.csv',
    'sheet': 'A',
  },
  {
    'input': './input/11-CarRental.XLS',
    'output': './output/car-rental.csv',
    'sheet': 'A',
  },
  {
    'input': './input/12-HousingTrust.XLS',
    'output': './output/housing-trust.csv',
    'sheet': 'A',
  },
  {
    'input': './input/14-AcuteCareHospAssess.XLS',
    'output': './output/acute-care-hosp-assess.csv',
    'sheet': 'A',
  },
  {
    'input': './input/390-Pension.XLS',
    'output': './output/pension.csv',
    'sheet': 'A',
  },
  {
    'input': './input/690-Residual.XLS',
    'output': './output/residual.csv',
    'sheet': 'A',
  },
]

CLASSES = {
  '100': 'Personal Services',
  '200': 'Purchase of Services',
  '300': 'Materials, Supplies & Equip.',
  '500': 'Contrib., Indemnities & Taxes',
  '800': 'Payments to Other Funds',
  '900': 'Advances & Miscellaneous Payments',
}

def float_or_zero(str):
  if str: return float(str)
  else: return 0

for fund in FUNDS:
  workbook = open_workbook(fund['input'])
  sheet = workbook.sheet_by_name(fund['sheet'])

  # Convert rows to list
  rows = []
  for row_index in range(sheet.nrows):
    rows.append(sheet.row_values(row_index))

  # Remove unneeded rows at top
  rows = rows[6:]

  # Only keep columns A and C through K
  rows = [[row[0]] + row[2:11] for row in rows]

  # Remove empty rows
  rows = [row for row in rows if any(row)]

  # Convert "department sections" to individual department rows using FY17 amount
  new_rows = [['Department', 'Class ID', 'Class', 'Total']]

  current_dept = ''
  for row in rows:
    label = row[0]

    if label.startswith('FY17'):
      total_class_100 = float_or_zero(row[1]) + float_or_zero(row[2]) + float_or_zero(row[3])
      total_class_300 = float_or_zero(row[5]) + float_or_zero(row[6])
      if total_class_100: new_rows.append([current_dept, 100, CLASSES['100'], total_class_100])
      if row[5]: new_rows.append([current_dept, 200, CLASSES['200'], row[5]])
      if total_class_300: new_rows.append([current_dept, 300, CLASSES['300'], total_class_300])
      if row[7]: new_rows.append([current_dept, 500, CLASSES['500'], row[7]])
      if row[8]: new_rows.append([current_dept, 800, CLASSES['800'], row[8]])
      if row[9]: new_rows.append([current_dept, 900, CLASSES['900'], row[9]])
    elif not label.startswith('FY16') and not label.startswith('INCREASE'):
      current_dept = label

  with open(fund['output'], 'wb') as f:
    writer(f).writerows(new_rows)

  print('Wrote {0} rows to {1}'.format(len(new_rows), fund['output']))
