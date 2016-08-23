/**
 * Convert letter to number, ie. AA becomes 27
 * http://stackoverflow.com/a/20169385/633406
 */
var letterIndex = function(x) {
    var result = 0;
    var multiplier = 1;
    for ( var i = x.length-1; i >= 0; i--) { 
        var value = ((x[i].charCodeAt(0) - "A".charCodeAt(0)) + 1);
        result = result + value * multiplier;
        multiplier = multiplier * 26;
    }
    return result;
};

/**
 * Converts excel index to Common Spreadsheet Format (CSF)
 * ex. B5 becomes {c:1, r:4}
 * ex. A3:B7 becomes {s:{c:0, r:2}, e:{c:1, r:6}}
 */
var rangeToCsf = function(range) {
	var indices = range.split(':')
		cells = [];
	indices.forEach(function(index) {
		var parts = index.match(/\D+|\d+/g);
		cells.push({c: letterIndex(parts[0]) - 1, r: parts[1] - 1});
	});
	return cells.length > 1 ? {s: cells[0], e: cells[1]} : cells[0];
};

module.exports = rangeToCsf;