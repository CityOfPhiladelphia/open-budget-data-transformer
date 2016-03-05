CLASS_MATCHES = {
  'Personal Services': {
    'id': 100,
    'name': 'Personal Services',
  },
  'Pers. Svcs.-Emp.Benefits': {
    'id': 100,
    'name': 'Personal Services',
  },
  'Purchase of Services': {
    'id': 200,
    'name': 'Purchase of Services',
  },
  'Materials, Supplies & Equip.': {
    'id': 300,
    'name': 'Materials, Supplies & Equip.',
  },
  'Contrib., Indemnities & Taxes': {
    'id': 500,
    'name': 'Contrib., Indemnities & Taxes',
  },
  'Debt Service': {
    'id': 700,
    'name': 'Debt Service',
  },
  'Payments to Other Funds': {
    'id': 800,
    'name': 'Payments to Other Funds',
  },
  'Advances & Miscellaneous Payments': {
    'id': 900,
    'name': 'Advances & Miscellaneous Payments',
  },
  'Advances and Other Misc. Payments': {
    'id': 900,
    'name': 'Advances & Miscellaneous Payments',
  }
}

CLASS_NAMES = {
  '100': 'Personal Services',
  '200': 'Purchase of Services',
  '300': 'Materials, Supplies & Equip.',
  '500': 'Contrib., Indemnities & Taxes',
  '700': 'Debt Service',
  '800': 'Payments to Other Funds',
  '900': 'Advances & Miscellaneous Payments',
}

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
