from __future__ import print_function
from yaml import load as load_yaml

import sys

class DepartmentNormalizer(object):

    department_aliases = {}

    def __init__(self, file_path):
        department_aliases = self.load(file_path)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            rows = load_yaml(f)

        for row in rows:
            if isinstance(row, dict):
                for name, variations in row.iteritems():
                    self.department_aliases[name.lower()] = name
                    for variation in variations:
                        self.department_aliases[variation.lower()] = name
            else:
                self.department_aliases[row.lower()] = row

    def get_normalized_name(self, department_alias):
        normalized_name = None
        alias_tail = department_alias
        while alias_tail != "" and not normalized_name:
            try:
                normalized_name = self.department_aliases[alias_tail.lower()]
            except:
                alias_tail = u'\u2013'.join(alias_tail.split(u"\u2013")[1:]).strip()
        return normalized_name

if __name__ == "__main__":
    pass