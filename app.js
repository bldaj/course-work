var express = require('express');
var app = express();

require('./routes/index')(app);

app.listen(9090, function () {
    console.log('App listening at port 9090');
});
