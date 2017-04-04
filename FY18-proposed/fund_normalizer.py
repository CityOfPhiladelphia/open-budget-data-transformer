from yaml import load as load_yaml

class FundNormalizer(object):

    def __init__(self, file_path):
        self.fund_aliases = self.load(file_path)

    def load(self, file_path):
        fund_aliases = {}
        with open(file_path, 'rb') as f:
            rows = load_yaml(f)

        for row in rows:
            if isinstance(row, dict):
                for name, variations in row.iteritems():
                    fund_aliases[name.lower()] = name
                    for variation in variations:
                        fund_aliases[variation.lower()] = name
            else:
                fund_aliases[row.lower()] = row
        return fund_aliases

    def get_normalized_name(self, fund_alias):
        normalized_name = self.fund_aliases[fund_alias.lower()]
        return normalized_name

if __name__ == "__main__":
    pass