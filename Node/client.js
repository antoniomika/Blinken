var //newrelic = require('newrelic'),
    WebSocket = require('ws'),
    rl = require('readline'),
    spawn = require('child_process').spawn;

var ws = new WebSocket("ws://" + process.argv[2] + "/ws/stream");
var child;

ws.on('open', function() {
    console.log("Opened!");
    child = spawn("/usr/bin/python", ["-u", "../Python/camera.py"]);
    var linereader = rl.createInterface(child.stdout, child.stdin);
    linereader.on('line', function(data) {
        ws.send(JSON.stringify({
            "time": new Date().getTime(),
            "data": data
        }));
    });
    child.on("error", function(err) {
        console.log(err);
    });
});

ws.on("message", function(data) {
    try {
        dataa = JSON.parse(data);
        if (dataa.pass == "h4x0r") {
            child.stdin.write(data + "\n");
        }
    } catch (err) {

    }
});