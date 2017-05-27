var getCVENames = require('../services');
var getFromJSONFile = require('../services');


module.exports = function (req, res) {
    var names = getCVENames();

    names.forEach(function (name) {
        if (req.params.year === name.slice(4)) {
            res.send(getFromJSONFile(name, 'cve-id'));
        }
    });
};