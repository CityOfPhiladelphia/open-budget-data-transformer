from csv import writer

from xlrd import open_workbook

FUNDS = [
  {
    'name': 'County Liquid Fuels Tax Fund',
    'input': './input/04-CountyLiq.XLS',
    'output': './output/county-liquid.csv',
    'sheet': 'A',
  },
  {
    'name': 'Special Gasoline Tax Fund',
    'input': './input/05-SpecGas.XLS',
    'output': './output/spec-gas.csv',
    'sheet': 'A',
  },
  {
    'name': 'Health Choices Behavioral Health Fund',
    'input': './input/06-HealthCh.XLS',
    'output': './output/health-ch.csv',
    'sheet': 'A',
  },
  {
    'name': 'Hotel Room Rental Tax Fund',
    'input': './input/07-Hotel.XLS',
    'output': './output/hotel.csv',
    'sheet': 'A',
  },
  {
    'name': 'Grants Revenue Fund',
    'input': './input/08-Grants.XLS',
    'output': './output/grants.csv',
    'sheet': 'A',
  },
  {
    'name': 'Aviation Fund',
    'input': './input/09-Aviation.XLS',
    'output': './output/aviation.csv',
    'sheet': 'A',
  },
  {
    'name': 'Community Development Fund',
    'input': './input/10-CommDev.XLS',
    'output': './output/comm-dev.csv',
    'sheet': 'A',
  },
  {
    'name': 'Car Rental Tax Fund',
    'input': './input/11-CarRental.XLS',
    'output': './output/car-rental.csv',
    'sheet': 'A',
  },
  {
    'name': 'Housing Trust Fund',
    'input': './input/12-HousingTrust.XLS',
    'output': './output/housing-trust.csv',
    'sheet': 'A',
  },
  {
    'name': 'Acute Care Hospital Assessment Fund',
    'input': './input/14-AcuteCareHospAssess.XLS',
    'output': './output/acute-care-hosp-assess.csv',
    'sheet': 'A',
  },
  {
    'name': 'Pension Fund',
    'input': './input/390-Pension.XLS',
    'output': './output/pension.csv',
    'sheet': 'A',
  },
  {
    'name': 'Water Residual Fund',
    'input': './input/690-Residual.XLS',
    'output': './output/residual.csv',
    'sheet': 'A',
  },
]

CLASS_NAMES = {
  '100': 'Personal Services',
  '200': 'Purchase of Services',
  '300': 'Materials, Supplies & Equip.',
  '500': 'Contrib., Indemnities & Taxes',
  '700': 'Debt Service',
  '800': 'Payments to Other Funds',
  '900': 'Advances & Miscellaneous Payments',
}

def float_or_zero(str):
  if str: return float(str)
  else: return 0

def construct_dept_rows(dept, row):
  dept_rows = []

  if row[u'CLASS 100'] or row[u'PENSIONS'] or row[u'OTHER FB']:
    total_class_100 = float_or_zero(row[u'CLASS 100']) + float_or_zero(row[u'PENSIONS']) + float_or_zero(row[u'OTHER FB'])
    dept_rows.append([dept, 100, CLASS_NAMES['100'], total_class_100])
  if row[u'CLASS 300'] or row[u'CLASS 400']:
    total_class_300 = float_or_zero(row[u'CLASS 300']) + float_or_zero(row[u'CLASS 400'])
    dept_rows.append([dept, 300, CLASS_NAMES['300'], total_class_300])

  for key in ['200', '500', '700', '800', '900']:
    if row.get(u'CLASS ' + key):
      dept_rows.append([dept, key, CLASS_NAMES[key], row[u'CLASS ' + key]])

  return dept_rows

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

  # Convert list of lists to list of dicts
  keys = rows[0]
  rows = rows[1:]
  rows = [dict(zip(keys, row)) for row in rows]

  # Convert "department sections" to individual department rows using FY17 amount
  new_rows = [['Department', 'Class ID', 'Class', 'Total']]

  current_dept = ''
  for row in rows:
    label = row[u'Department']

    if label.startswith('FY17'):
      new_rows = new_rows + construct_dept_rows(current_dept, row)
    elif not label.startswith('FY16') and not label.startswith('INCREASE') and not label.startswith('TOTAL'):
      current_dept = label

  # Add year and fund columns to each row
  new_rows[0] = ['Fiscal Year', 'Fund'] + new_rows[0]
  new_rows = [new_rows[0]] + [['2017', fund['name']] + row for row in new_rows[1:]]

  with open(fund['output'], 'wb') as f:
    writer(f).writerows(new_rows)

  print('Wrote {0} rows to {1}'.format(len(new_rows), fund['output']))
