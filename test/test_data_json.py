import json

import yaml
import nose

CONFIG_FILE_PATH = './test/config_fy17.yml'
DATA_FILE_PATH = './output/data.json'

with open(CONFIG_FILE_PATH) as config_file:
  tests = yaml.load(config_file)

with open(DATA_FILE_PATH) as data_file:
  data_rows = list(json.load(data_file))

def test_fn():
  for test in tests:
    matches = [
      class_['gross_cost']['accounts']['2017']
      for fund in data_rows if fund['name'] == test['Fund']
      for dept in fund['children'] if dept['name'] == test['Department']
      for class_ in dept['children'] if class_['name'] == test['Class']
    ]
    match_count = len(matches)
    printable_representation = test.values()

    if test['Total'] == 0:
      yield nose.tools.ok_, (match_count == 0 or matches[0] == 0), 'Found {0} non-zero records for {1}'.format(match_count, printable_representation)
    else:
      yield nose.tools.assert_equals, match_count, 1, '{0} records for {1}'.format(match_count, printable_representation)
      if match_count:
        yield nose.tools.assert_equals, matches[0], test['Total'], 'Incorrect total for {0}'.format(printable_representation)
