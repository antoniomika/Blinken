var //newrelic = require('newrelic'),
    WebSocket = require('ws'),
    spawn = require('child_process').spawn;

var ws = new WebSocket("ws://" + process.argv[2] + "/ws/stream");

ws.on('open', function() {
    console.log("Opened!");
    var child = spawn("/usr/bin/raspivid", ["-t", "0", "-w", "300", "-h", "300", "-hf", "-fps", "20", "-o", "-"]);
    child.stdout.on("data", function(data) {
        ws.send(JSON.stringify({
            "time": new Date().getTime(),
            "data": data.toString("base64")
        }));
    });
});
