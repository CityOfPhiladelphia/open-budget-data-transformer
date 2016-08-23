# open-budget-data-transformer
Master repo of data cleanup scripts for the various budget cycles

The City operating budget is refreshed twice per fiscal year: first when it is
proposed to City Council in March, and second when it is adopted around June/July.
The proposed budget is provided as a spreadsheet(s) formatted for print. The
adopted budget is provided as a well-formed CSV file. The goal of these scripts
is to (a) transform the data provided into a consistent format (including some
modifications requested by the Budget Office), and (b) transform it further into
a format called **flare.json**, which allows it to be used in the
[open-budget](https://github.com/cityofphiladelphia/open-budget) application.

This repository is divided into a directory for each budget cycle. The
`FY16-proposed` and `FY17-proposed` operate on such drastically different source
files that they should not be merged. The `FY17-adopted` script, however, should
be adapted to work on any fiscal year since the adopted budget always comes from
the same source. These directories are all meant to generate a file in a consistent
format:

```
fiscal_year | fund | department | class_id | class | minor_class_id | minor_class | total
```

The `flare` directory is meant to take two years worth of data (representing the
same cycle) and output a single `data.json` file, which can be put into the
open-budget application.

Each directory has usage instructions inside its `README.md`.
