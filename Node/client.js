var //newrelic = require('newrelic'),
    WebSocket = require('ws'),
    spawn = require('child_process').spawn;

var ws = new WebSocket("ws://" + process.argv[2] + "/ws/stream");

var heldFrame = "";

ws.on('open', function() {
    console.log("Opened!");
    var child = spawn("/usr/bin/python", ["-u", "../Python/camera.py"]);
    child.stdout.on("data", function(data) {
        var sendData = data.toString();
        if(sendData.length >= 65535) {
            heldFrame = heldFrame + sendData;
        } else if(sendData.length > 10) {
            ws.send(JSON.stringify({
                "time": new Date().getTime(),
                "data": heldFrame + sendData
            }));
            heldFrame = "";
        } else {
            ws.send(JSON.stringify({
                "time": new Date().getTime(),
                "data": sendData
            }));
        }
    });
    child.on("error", function(err) { console.log(err); });
});
