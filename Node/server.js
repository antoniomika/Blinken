var newrelic = require('newrelic'),
    http = require('http'),
    express = require('express'),
    request = require('request'),
    app = express(),
    server = http.createServer(app),
    morgan = require('morgan'),
    bodyParser = require('body-parser'),
    WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({
        server: server
    }),
    url = require("url");

morgan.token('remote-addr', function(req, res) {
    return req.headers['x-forwarded-for'] || req.ip;
});

app.use(morgan("combined"));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: false
}));

app.use(express.static('static'));

wss.on('connection', function connection(ws) {
    var location = url.parse(ws.upgradeReq.url, true);
    var uip = ws.upgradeReq.headers['x-forwarded-for'] || ws.upgradeReq.connection.remoteAddress;

    switch(location["pathname"]) {
        case "/ws/view":
            break;
        case "/ws/stream":
            ws.on("message", function(message) {
                console.log(wss.clients.length);
                wss.clients.forEach(function each(client) {
                    var location = url.parse(client.upgradeReq.url, true);

                    switch(location["pathname"]) {
                        case "/ws/view":
                            client.send(message);
                            break;
                        default:
                            break;
                    }
                });
            })
            break;
        default:
            ws.close();
            break;
    }

    ws.on('error', function(err) {
        console.log(err);
    });
});

wss.on('error', function(err) {
    console.log(err);
});

server.listen(process.env.PORT || 8080, function() {
    console.log("Listening on port:", process.env.PORT || 8080);
});
