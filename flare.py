################
# Generate flare
# 
# 1. Read in files as list of dicts
# 
# 2. For each file
  # a. Group by Fund-Department-Class
  # b. Instead of 2 "Total" properties, one for each file that represents its year
    # format: ConcatKey: {Fund, Department, Class ID, Class, 2016, 2017}
# 
# 3. Generate nested d3 flare from data.values()
# 
# 4. Sort the flare descending by the latest year's totals
#################

import json
import csv
from collections import defaultdict
import random

INPUT_FILES = [
  {
    'fiscal_year': '2016',
    'path': './output/FY2016-proposed.csv',
  },
  {
    'fiscal_year': '2017',
    'path': './output/FY2017-proposed.csv',
  },
]

def nest(rows, keys, current_index=0, sort_by=None):
  key = keys[current_index]

  # Create the structure of what's returned
  grouped_rows = defaultdict(lambda: {
    'children': [],
    'gross_cost': {
      'accounts': defaultdict(int)
    }
  })

  # Group rows by the current key
  for row in rows:
    group_dict = grouped_rows[row[key]]
    group_dict['id'] = random.randrange(1, 999)
    group_dict['name'] = row[key]
    group_dict['gross_cost']['accounts'][row['Fiscal Year']] += int(row['Total'])
    group_dict['children'].append(row)

  # For each grouping, recurse on its children until at last key
  for key, val in grouped_rows.iteritems():
    if len(keys) > current_index + 1:
      val['children'] = nest(val['children'], keys, current_index=current_index + 1, sort_by=sort_by).values()
      if sort_by:
        val['children'].sort(key=lambda row: -row['gross_cost']['accounts'][sort_by])
    else:
      del(val['children'])
  
  return grouped_rows

# Read files into one list of dicts
rows = []
for file in INPUT_FILES:
  with open(file['path'], 'rb') as file:
    rows = rows + list(csv.DictReader(file))

# Nest the list by list of keys recursively
nested_rows = nest(rows, ['Fund', 'Department', 'Class'], sort_by='2017').values()

print(json.dumps(nested_rows, indent=2, sort_keys=True))
