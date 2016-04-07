var //newrelic = require('newrelic'),
    WebSocket = require('ws'),
    spawn = require('child_process').spawn;

var ws = new WebSocket("ws://" + process.argv[2] + "/ws/stream");

ws.on('open', function() {
    console.log("Opened!");
    var child = spawn("python", ["../Python/camera.py"]);
    child.stdout.on("data", function(data) {
        ws.send(JSON.stringify({
            "time": new Date().getTime(),
            "data": data
        }));
    });
});
