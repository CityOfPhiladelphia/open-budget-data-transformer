from re import sub

from titlecase import titlecase
from yaml import load as load_yaml

class CleanDepartments(object):
  def __init__(self, file_path):
    if(file_path): self.matches = self.load(file_path)

  def load(self, file_path):
    matches = {}

    with open(file_path, 'rb') as file:
      rows = load_yaml(file)

      for row in rows:
        if isinstance(row, dict):
          # If it's a dict, add a match for the key, and for each of the values
          for name, variations in row.iteritems(): # only one of these
            matches[name] = name
            for variation in variations:
              matches[variation] = name
        else:
          # Otherwise it's just a string; add a match for it
          matches[row] = row

    return matches

  def clean(self, dept):
    dashes_replaced = sub(r'(?! )-(?! )', ' - ', dept)
    title_cased = titlecase(dashes_replaced)
    match = self.matches.get(title_cased)
    if not match: raise KeyError('No match found for {0}'.format(title_cased))
    return match
