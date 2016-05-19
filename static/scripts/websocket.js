var websocket = {};

websocket.connect = function(update) {
    var ws = new WebSocket("ws://localhost:5000");
    ws.onopen = function(evt) {
        gui.serverMessage("Connected to server.");
    };

    ws.onerror = function(err) {
        gui.serverMessage("Could not connect to server.");
    };

    ws.onmessage = function(evt) {
        json = JSON.parse(evt.data);
        for (var i in json.node) {
            var pos = json.node[i].position;
            json.node[i].position = new THREE.Vector3(pos.x, pos.y, pos.z);
        }
        update(json);
    };

    ws.onclose = function(evt) {
        gui.serverMessage("Connection to server lost. <a href='#' onclick='javascript:websocket.connect()'>Reconnect</a>.", true);
    };
};
