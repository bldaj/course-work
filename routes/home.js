var getCVENames = require('../services');

module.exports = function (req, res) {
    res.write('Available CVE-s\n');

    var names = getCVENames();

    names.forEach(function (name, i) {
        res.write(i + ': ' + name + '\n');
    });

    res.end();
};