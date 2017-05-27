module.exports = function (app) {
    app.get('/', require('./home'));
    app.get('/:year', require('./cveForYear'));
    app.get('/:year/cve-id', require('./cveIdsForYear'));
};