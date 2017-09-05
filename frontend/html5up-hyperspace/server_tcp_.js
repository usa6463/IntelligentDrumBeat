
/*
var net = require('net');

var HOST = '127.0.0.1';
var PORT = 6969;

// Create a server instance, and chain the listen function to it
// The function passed to net.createServer() becomes the event handler for the 'connection' event
// The sock object the callback function receives UNIQUE for each connection
net.createServer(function(sock) {
    
    // We have a connection - a socket object is assigned to the connection automatically
    console.log('CONNECTED: ' + sock.remoteAddress +':'+ sock.remotePort);
    
    // Add a 'data' event handler to this instance of socket
    sock.on('data', function(data) {
        
        console.log('DATA ' + sock.remoteAddress + ': ' + data);
        // Write the data back to the socket, the client will receive it as data from the server
        sock.write('You said "' + data + '"');
        
    });
    
    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        console.log('CLOSED: ' + sock.remoteAddress +' '+ sock.remotePort);
    });
    
}).listen(PORT, HOST);

console.log('Server listening on ' + HOST +':'+ PORT);
*/

var net = require('net');
var fs = require('fs');
var buffer = require('buffer');

var server = net.createServer(function(conn) {
    console.log('server connected');

});

var HOST = '127.0.0.1';
var PORT = '9001'
var FILEPATH = '/home/steve/Downloads/';

server.listen(PORT, HOST, function() {
    //listening
    console.log('server bound to ' + PORT + '\n');

    server.on('connection', function(conn) {
        console.log('connection made...\n')
        conn.on('data', function(data) {
            console.log('data received');
            console.log('data is: \n' + data);
        });
    })
});