var services = require('./services');

module.exports = function (app) {
    app.get('/', function (req, res) {
        res.write('Available CVE-s\n');

        var names = services.getCVENames();

        names.forEach(function (name, i) {
            res.write(i + ': ' + name + '\n');
        });

        res.end();
    });

    app.get('/:year', function (req, res) {
        var year = req.params.year;
        var result = services.getCVENamesForYear(year);

        if (result.length) {
            res.send(services.getFromJSONFile(result[0]));
        } else {
            res.send("Nothing found");
        }
    });

    app.get('/:year/cve-ids', function (req, res) {
        var names = services.getCVENames();

        names.forEach(function (name) {
            if (req.params.year === name.slice(4)) {
                res.send(services.getFromJSONFile(name, 'cve-id'));
            }
        });
    });
};
