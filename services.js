var MongoClient = require('mongodb').MongoClient;

const url = 'mongodb://localhost:27017/CVE';
const CVENames = [
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
    return CVENames;
};

var getDataFromCVECollection = function (CVECollection) {
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
            db.collection(CVECollection).find().toArray(function (err, result) {
                if (err) {
                    reject(err);
                } else {
                    resolve(result);
                }
            })
        })
    })
};

var findCVECollectionByCVEName = function(year) {
    var names = getCVENames();

    return names.filter(function (name) {
        return year === name.slice(4)
    })
};

var getCVECollection = function (CVEName) {
    return findCVECollectionByCVEName(CVEName)[0]
};

module.exports.getDataFromCVECollection = getDataFromCVECollection;
module.exports.getCVECollection = getCVECollection;
module.exports.getCVENames = getCVENames;