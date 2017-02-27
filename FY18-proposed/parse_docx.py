import docx2txt
import re
import sys

FUND_NAME_REGEX = re.compile("[A-Z]+( [A-Z]+)+")
DEPARTMENT_NAME_REGEX = re.compile("\d+\.\d+\s+TO\s+(.+)")
CLASS_NAME_AND_AMOUNT_REGEX = re.compile("([a-zA-Z ,-]+)\s+(?:\$\s+)?([0-9,]+)$")

if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except:
        print "Please pass the path to the budget docx file."

    with open(fname) as f:
        budget_doc = docx2txt.process(f)

    current_fund = ""
    department_name = ""
    class_name = ""
    subtotal = 0
    for budget_line in budget_doc.splitlines():
        budget_line = budget_line.strip()
        match = None

        # Is this a new section?
        if budget_line.startswith("SECTION"):
            match = FUND_NAME_REGEX.search(budget_line)
            if match:
                fund_name = match.group(0)
                print "Fund name:", fund_name
            continue

        # Is this a subsection with a department name?
        match = DEPARTMENT_NAME_REGEX.match(budget_line)
        if match:
            department_name = match.group(1)
            print "Department name:", department_name.encode("UTF-8")
            continue

        # Is it a class subentry or total line?
        match = CLASS_NAME_AND_AMOUNT_REGEX.match(budget_line)
        if match:
            class_name = match.group(1).strip()
            amount = int(match.group(2).replace(',', ''))
            if class_name == "Total":
                if subtotal != amount:
                    raise Exception("sub != total", class_name, subtotal, amount)
                print "Total", subtotal, amount
                subtotal = 0
            else:
                subtotal += amount
                print class_name, amount
