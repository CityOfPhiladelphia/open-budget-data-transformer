from __future__ import print_function
import csv
from sys import stdin, stdout, stderr

from clean_departments import CleanDepartments

DEPARTMENTS_FILE_PATH = './departments.yml'

header = ['fiscal_year', 'fund', 'department', 'class_id',
          'class', 'subclass_id', 'subclass', 'total']

def clean_fund (row):
    fund = row['fund']

    corrected_fund = fund \
        .replace(' Operating', '') \
        .replace('Healthchoices', 'Healthy Choices') \
        .replace('Airport', 'Aviation')

    return corrected_fund

def clean_department (row):
    # Load departments and their matches
    clean_departments = CleanDepartments(DEPARTMENTS_FILE_PATH)
    department = row['department']

    if ('Office of Technology' in department):
        department = 'Office of Innovation & Technology'

    try:
        clean_dept = clean_departments.clean(department)
    except KeyError as e:
        print(e, file=stderr)
        return ''

    return clean_dept

rows = csv.DictReader(stdin)
writer = csv.DictWriter(stdout, fieldnames=header)
writer.writeheader()

for row in rows:
    clean_row = {
        'fiscal_year': row['fiscal_year'],
        'fund': clean_fund(row),
        'department': clean_department(row),
        'class_id': row['class_id'],
        'class': row['class'],
        'subclass_id': row['minor_class_id'],
        'subclass': row['minor_class'],
        'total': row['total']
    }
    writer.writerow(clean_row)
