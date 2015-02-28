# Open Budget Trends Parser
Parses the giant `FY16 Budget Trends.xlsx` spreadsheet the Budget Office uses into a CSV format with one record for every year-fund-department-class for use in visualizations

## Configuration
Map the excel table ranges into `config.js` (include the header row, but don't include the row at the bottom with totals)

## Usage
Put the `.xlsx` file in the `data` directory (there's already one there) and make sure `transform.js` points to the write filename (it already does)
```bash
$ node transform.js
```
Will build `data.csv` in the `data` directory