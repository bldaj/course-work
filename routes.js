var services = require('./services');

module.exports = function (app) {
    app.get('/', function (req, res) {
        res.send(services.getCVENames());
    });

    app.get('/:CVEName', function (req, res) {
        var CVECollection = services.getCVECollection(req.params.CVEName);

        if (CVECollection) {
            services.getDataFromCVECollection(CVECollection).then(function (data) {
                res.send(data);
            });
        } else {
            res.send("Nothing found");
        }
    });
};