var getCVENames = require('./services');
var getFromJSONFile = require('./services');
var getCVENamesForYear = require('./services');


module.exports = function (app) {
    app.get('/', function (req, res) {
        res.write('Available CVE-s\n');

        var names = getCVENames();

        names.forEach(function (name, i) {
            res.write(i + ': ' + name + '\n');
        });

        res.end();
    });

    app.get('/:year', function (req, res) {
        var year = req.params.year;
        var result = getCVENamesForYear(year);

        if (result.length) {
            res.send(getFromJSONFile(result[0]));
        } else {
            res.send("Nothing found");
        }
    });

    app.get('/:year/cve-id', function (req, res) {
        var names = getCVENames();

        names.forEach(function (name) {
            if (req.params.year === name.slice(4)) {
                res.send(getFromJSONFile(name, 'cve-id'));
            }
        });
    });
}();