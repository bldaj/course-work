var express = require('express');

var app = express();

app.listen(9090, function () {
    console.log('App listening at port 9090');
});

require('./routes.js')(app);
