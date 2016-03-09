import csv

import yaml
import nose

CONFIG_FILE_PATH = './test/config_fy17.yml'
DATA_FILE_PATH = './output/FY2017-proposed.csv'

with open(CONFIG_FILE_PATH) as config_file:
  tests = yaml.load(config_file)

with open(DATA_FILE_PATH) as data_file:
  data_rows = list(csv.DictReader(data_file))

def test_fn():
  for test in tests:
    results = [row for row in data_rows if all(row[key] == str(value) for key, value in test.items())]
    yield nose.tools.assert_equals, len(results), 1, 'Could not find {0}'.format(test.values())
