import csv
import json

import click
import yaml

def row_matches_test(row, test):
    return all(row[key] == str(value) for key, value in test.items() if key != 'total')

@click.group()
def cli():
    pass

@cli.command('csv')
@click.argument('data_path', type=click.Path(exists=True))
@click.argument('tests_path', type=click.Path(exists=True))
def validate_csv(data_path, tests_path):
    with open(data_path) as data_file:
        data = list(csv.DictReader(data_file))

    with open(tests_path) as tests_file:
        tests = yaml.load(tests_file)

    for test in tests:
        results = [row for row in data if row_matches_test(row, test)]

        try:
            if test['total'] == 0:
                assert len(results) == 0, 'Found {0} records for {1} expected 0'.format(len(results), list(test.values()))
            else:
                assert len(results) == 1, '{0} records for {1}'.format(len(results), list(test.values()))
                assert results[0]['total'] == str(test['total']), 'Incorrect total for {2}'.format(test['total'], results[0]['total'], list(test.values()))
        except AssertionError as e:
            print(e.args[0])

@cli.command('json')
@click.argument('data_path', type=click.Path(exists=True))
@click.argument('tests_path', type=click.Path(exists=True))
@click.argument('year')
def validate_json(data_path, tests_path, year):
    with open(data_path) as data_file:
        data = list(json.load(data_file))

    with open(tests_path) as tests_file:
        tests = yaml.load(tests_file)

    for test in tests:
        matches = [
            class_['gross_cost']['accounts'][year]
            for fund in data if fund['name'] == test['fund']
            for dept in fund['children'] if dept['name'] == test['department']
            for class_ in dept['children'] if class_['name'] == test['class']
        ]
        match_count = len(matches)
        printable_representation = list(test.values())

        try:
            if test['total'] == 0:
                assert (match_count == 0 or matches[0] == 0), 'Found {0} non-zero records for {1}'.format(match_count, printable_representation)
            else:
                assert match_count == 1, '{0} records for {1}'.format(match_count, printable_representation)
                if match_count:
                    assert matches[0] == test['total'], 'Incorrect total for {0}'.format(printable_representation)
        except AssertionError as e:
            print(e.args[0])

if __name__ == '__main__':
    cli()
