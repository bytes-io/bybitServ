/*
Dependencies: bitcore (global), unirest (almost global),
>> check taht unirest and bitcore-lib are front-end compatible
// browsify to compile
> bluebird - is a promise library
> unirest - is a http request
> JQUERY deferred vs. promise
> management of asynchronicity
Primise.each(<iterator>, (returns a promise))
*/

// DEPENDENCIES
var WebSocket = require('ws');

    ws= new WebSocket("ws://localhost:7878/echo");

    ws.on('error', function(error){ console.log('Communication problem')})

    ws.onopen = function(e) {
      console.log('Connection to server opened');
      ws.send('ae0')
      ws.send('ae1')
      ws.send('ae2')
    }

    ws.onmessage = function(e) {
      console.log('msg received!:', e.data)
    }

    ws.onclose = function(e) { console.log("Connection closed") }
