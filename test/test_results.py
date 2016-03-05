import csv

import yaml
import nose

CONFIG_FILE_PATH = './test/config.yml'
GENERAL_FUND_FILE_PATH = './output/general-fund.csv'

with open(CONFIG_FILE_PATH) as config_file:
  tests = yaml.load(config_file)

with open(GENERAL_FUND_FILE_PATH) as general_fund_file:
  general_fund_rows = list(csv.DictReader(general_fund_file))

def test_fn():
  for test in tests:
    results = [row for row in general_fund_rows if all(row[key] == str(value) for key, value in test.items())]
    yield nose.tools.assert_equals, len(results), 1, 'Could not find {0}'.format(test.values())
