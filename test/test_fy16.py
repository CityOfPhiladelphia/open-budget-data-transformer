import csv

import yaml
import nose

CONFIG_FILE_PATH = './test/config_fy16.yml'
DATA_FILE_PATH = './output/FY2016-proposed.csv'

with open(CONFIG_FILE_PATH) as config_file:
  tests = yaml.load(config_file)

with open(DATA_FILE_PATH) as data_file:
  data_rows = list(csv.DictReader(data_file))

def test_fn():
  for test in tests:
    results = [row for row in data_rows if all(row[key] == str(value) for key, value in test.items() if key != 'Total')]
    if test['Total'] == 0:
      yield nose.tools.assert_equals, len(results), 0, 'Found {0} records for {1} expected 0'.format(len(results), test.values())
    else:
      yield nose.tools.assert_equals, len(results), 1, '{0} records for {1}'.format(len(results), test.values())
      yield nose.tools.assert_equals, results[0]['Total'], str(test['Total']), 'Incorrect total for {2}'.format(test['Total'], results[0]['Total'], test.values())
