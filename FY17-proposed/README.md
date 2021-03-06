# Open Budget 2017 Parser 
Parses the MS Excel spreadsheets the Budget Office uses into a CSV format with one record for 
every year-fund-department-class for use in the
[open-budget](https://github.com/cityofphiladelphia/open-budget) app.

# Installation
1. Clone this repo
2. Optionally, create a virtual environment using `virtualenv venv`
and activate it via `. venv/bin/activate`
3. Install dependencies via `pip install -r requirements.txt`

# Usage
First, process the general fund file and the other fund files
```sh
python general_fund.py
python other_funds.py
```
Then combine them into one FY17 file:
```sh
python combine_fy17.py
```
Then process the FY16 data:
```sh
python fy16.py
```
Finally, generate the flare JSON for the open budget app:
```sh
python flare.py > path/to/budget/app/data.json
```

# Production optimization
From [tpreusse/open-budget wiki](https://github.com/tpreusse/open-budget/wiki/Data-Format#cache-cachejson):
> For production you can create a cache with pre-processed values and without arbitrary data. 
> Call `OpenBudget.nodes.createCache()` via your browser console and save the output to your 
> data directory as `cache.json`. Cache is used whenever `cache_url` is specified in `meta.json`.
(Ideally this would be implemented in python inside this repo as well, but it is not currently.)

# Testing
This tool uses an easily-configurable [list of tests](test/config_fy17.yml) to
verify the data integrity, essentially automating "spot checking." To test the output
from the above commands, run:
```sh
nosetests
```
