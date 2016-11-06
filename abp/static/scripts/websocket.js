var websocket = {};
websocket.update = undefined;

websocket.connect = function(update) {
    websocket.ws = new WebSocket("ws://localhost:5000");
    if (update){
        websocket.update = update;
    }
    websocket.ws.onopen = function(evt) {
        gui.serverMessage("Connected to server.");
    };

    websocket.ws.onerror = function(err) {
        gui.serverMessage("Could not connect to server.");
    };

    websocket.ws.onmessage = function(evt) {
        json = JSON.parse(evt.data);
        for (var i in json.node) {
            var pos = json.node[i].position;
            json.node[i].position = new THREE.Vector3(pos.x, pos.y, pos.z);
            if (json.node[i].vop === undefined){
                json.node[i].vop = 0;
            }
        }
        websocket.update(json);
    };

    websocket.ws.onclose = function(evt) {
        gui.serverMessage("No connection to server. <a href='#' onclick='javascript:websocket.connect()'>Reconnect</a>.", true);
    };
};

websocket.edit = function (data) {
    websocket.ws.send("edit:"+JSON.stringify(data));
};
