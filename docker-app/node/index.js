
var express = require('express'),
    http = require('http'),
    redis = require('redis');

var app = express();

console.log(process.env.REDIS_PORT_6379_TCP_ADDR + ':' + process.env.REDIS_PORT_6379_TCP_PORT);


var client = redis.createClient(
process.env.REDIS_PORT_6379_TCP_PORT,
process.env.REDIS_PORT_6379_TCP_ADDR
);

app.get('/', function(req, res, next) {
  client.incr('visit-count', function(err, count) {
    if(err) return next(err);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.write('Hello World!\n');
    res.write('This page is viewed ' + count + ' times!');
    res.send();
  });
});


http.createServer(app).listen(3000, function() {
  console.log('Listening on port ' + (3000));
});
