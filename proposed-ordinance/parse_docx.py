from __future__ import print_function
import csv
import docx2txt
import re
import sys
import titlecase

from constants import CLASS_NAMES, CLASS_MATCHES
from department_normalizer import DepartmentNormalizer

FUND_NAME_REGEX = re.compile("[A-Z]+( [A-Z]+)+")
FUND_AMOUNT_REGEX = re.compile("\(([0-9,]+)\)")
DEPARTMENT_NAME_REGEX = re.compile("\d+\.\d+\s+TO(?:\s+THE)\s+(.+)")
CLASS_NAME_AND_AMOUNT_REGEX = re.compile("([a-zA-Z ,-]+)\s+(?:\$\s+)?([0-9,]+)$")

if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except:
        print("Please pass the path to the budget docx file.", file=sys.stderr)

    with open(fname, "rb") as f:
        budget_doc = docx2txt.process(f)

    normalizer = DepartmentNormalizer("./departments.yml")

    current_fund = ""
    department_name = ""
    class_name = ""
    subtotal = 0
    fund_subtotal = 0
    fund_amount = None
    rows = []
    for budget_line in budget_doc.splitlines():
        budget_line = budget_line.strip()
        match = None

        # Is this a new section?
        if budget_line.startswith("SECTION"):
            if fund_amount is not None:
                if fund_amount != fund_subtotal:
                    print(budget_line)
                    print(fund_amount, fund_subtotal)
                    raise Exception("Fund Grand Total != Fund Subtotal")
                fund_subtotal = 0
            match = FUND_NAME_REGEX.search(budget_line)
            if match:
                fund_name = titlecase.titlecase(match.group(0))
                # TODO get fund total
                match = FUND_AMOUNT_REGEX.search(budget_line)
                fund_amount = int(match.group(1).replace(',', ''))
            continue

        # Is this a subsection with a department name?
        match = DEPARTMENT_NAME_REGEX.match(budget_line)
        if match:
            department_alias = match.group(1).strip()
            department_name = normalizer.get_normalized_name(department_alias)
            if department_name is None or department_name.strip() == "":
                print(department_alias.encode("UTF8"), file=sys.stderr)
            continue

        # Is it a class subentry or total line?
        match = CLASS_NAME_AND_AMOUNT_REGEX.match(budget_line)
        if match:
            denormalized_class_name = match.group(1).strip()
            amount = int(match.group(2).replace(',', ''))
            if denormalized_class_name == "Total":
                if subtotal != amount:
                    raise Exception("sub != total", class_name, subtotal, amount)
                subtotal = 0
            else:
                class_match = CLASS_MATCHES[denormalized_class_name]
                class_name = class_match["name"]
                class_id = class_match["id"]
                subtotal += amount
                fund_subtotal += amount
                row = {"fiscal_year": 2019,
                       "fund": fund_name,
                       "department": department_name,
                       "class_id": class_id,
                       "class": class_name,
                       "total": amount}
                rows.append(row)

    field_names = ["fiscal_year", "fund", "department", "class_id", "class", "total"]
    dict_writer = csv.DictWriter(sys.stdout, field_names)
    dict_writer.writeheader()
    dict_writer.writerows(rows)
