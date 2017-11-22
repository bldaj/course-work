var MongoClient = require('mongodb').MongoClient;

var url = 'mongodb://localhost:27017/CVE';
var jsonNames = [
    'CVE-Modified', 'CVE-Recent',
    'CVE-2002', 'CVE-2003',
    'CVE-2004', 'CVE-2005',
    'CVE-2006', 'CVE-2007',
    'CVE-2008', 'CVE-2009',
    'CVE-2010', 'CVE-2011',
    'CVE-2012', 'CVE-2013',
    'CVE-2014', 'CVE-2015',
    'CVE-2016', 'CVE-2017'];

var getCVENames = function() {
    return jsonNames;
};

var getData = function (CVEname) {
    return new Promise(function (resolve, reject) {
        MongoClient.connect(url, function (err, db) {
            if (err) {
                reject(err);
            } else {
                resolve(db);
            }
        })
    }).then(function (db) {
        return new Promise(function (resolve, reject) {
            var collection = db.collection(CVEname);

            collection.find().toArray(function (err, result) {
                if (err) {
                    reject(err);
                } else {
                    resolve(result);
                }
            })
        })
    })
};

var getCVENamesForYear = function(year) {
    var names = getCVENames();

    return names.filter(function (name) {
        return year === name.slice(4);
    });
};

module.exports.getData = getData;
module.exports.getCVENamesForYear = getCVENamesForYear;
module.exports.getCVENames = getCVENames;
