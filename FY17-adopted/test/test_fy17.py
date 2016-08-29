import csv
from collections import defaultdict
from decimal import Decimal

import yaml
import nose

CONFIG_FILE_PATH = './test/config_fy17_adopted.yml'
DATA_FILE_PATH = './output/FY17-adopted.csv'

def aggregate (data, groupBy):
    grouped_dict = defaultdict(Decimal)
    for row in data:
        # key = tuple(row[field] for field in groupBy)
        key = (row['fund'], row['department'], row['class'])
        grouped_dict[key] += int(row['total'])
    return grouped_dict

with open(CONFIG_FILE_PATH) as config_file:
  tests = yaml.load(config_file)

with open(DATA_FILE_PATH) as data_file:
  data_rows = list(csv.DictReader(data_file))

aggregated_data_rows = aggregate(data_rows, ['fund', 'department', 'class'])

def test_fn():
  for test in tests:
    results = [row for row in aggregated_data_rows if all(row[key] == str(value) for key, value in test.items() if key != 'total')]
    if test['total'] == 0:
      yield nose.tools.assert_equals, len(results), 0, 'Found {0} records for {1} expected 0'.format(len(results), test.values())
    else:
      yield nose.tools.assert_equals, len(results), 1, '{0} records for {1}'.format(len(results), test.values())
      yield nose.tools.assert_equals, results[0]['total'], str(test['total']), 'Incorrect total for {2}'.format(test['total'], results[0]['Total'], test.values())
