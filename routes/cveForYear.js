var getFromJSONFile = require('../services');
var getCVENamesForYear = require('../services');


module.exports = function (req, res) {
    var year = req.params.year;
    var result = getCVENamesForYear(year);

    if (result.length) {
        res.send(getFromJSONFile(result[0]));
    } else {
        res.send("Nothing found");
    }
};