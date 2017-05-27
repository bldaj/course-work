var fs = require('fs');

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


exports.getFromJSONFile = function (jsonName, innerTag, outerTag) {
    var basePath = '/home/k/PyCharm Projects/parser/CVEs/JSONs/';
    var contents = fs.readFileSync(basePath + jsonName + '.json');
    var jsonContent = JSON.parse(contents);

    var resData = [];

    for (var i in jsonContent) {
        if (outerTag){
            resData.push(jsonContent[i][innerTag][outerTag]);
        }
        else {
            if (innerTag) {
                resData.push(jsonContent[i][innerTag]);
            }
            else {
                resData.push(jsonContent[i]);
            }
        }
    }

    return resData;
};

exports.getCVENames = function() {
    return jsonNames;
};

exports.getCVENamesForYear = function(year) {
    var names = module.getCVENames();

    return names.filter(function (name) {
        return year === name.slice(4);
    });
};
