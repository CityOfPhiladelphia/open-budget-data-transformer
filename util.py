from collections import defaultdict

# Group rows by everything but total and aggregate the total (sum)
def aggregate_similar_rows(rows, index):
  grouped_rows = defaultdict(int)

  for row in rows:
    aggregate_value = row.pop(index)
    key = tuple(row)
    grouped_rows[key] += int(float(aggregate_value))

  # Convert the grouped dict to a list of lists
  return [list(key) + [total] for key, total in grouped_rows.iteritems()]
