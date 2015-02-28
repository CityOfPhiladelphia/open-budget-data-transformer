var xlsx = require('xlsx'),
	fs = require('fs'),
	csv = require('fast-csv'),
	rangeToCsf = require('./range-to-csf'),
	config = require('./config.json'),
	classes = require('./classes.json');

var inputFile = './data/FY16 Budget Trends.xlsx',
	outputFile = './data/data.csv';

var workbook = xlsx.readFile(inputFile),
	sheet = workbook.Sheets[workbook.SheetNames[0]]
	records = [];

config.forEach(function(table) {
	var departments = xlsx.utils.sheet_to_json(sheet, {range: table.range});

	// Loop through each row in the table (there's one row per department)
	departments.forEach(function(dept) {
		// Loop through each key in the row
		for(var key in dept) {
			// If the key starts with 'Class' and the cell's contents is not 0, add a record for this department specific to this class
			if(key.substr(0, 5) === 'Class' && dept[key] != 0) {
				records.push({
					'Fiscal Year': table.fiscalYear,
					'Fund': table.fund,
					'Department': dept.Department,
					'Class ID': key.substr(6),
					'Class': classes[key.substr(6)] || '',
					'Total': dept[key].replace(/,/g, '').replace('(', '-').replace(')', '')
				});
			}
		}
	});
});

//console.log(records);
csv.writeToPath(outputFile, records, {headers: true})
.on('finish', function() {
	console.log(records.length + ' records written to ' + outputFile);
});