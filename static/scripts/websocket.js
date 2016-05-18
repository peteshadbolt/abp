var websocket = {};

websocket.connect = function(update){
    var ws = new WebSocket("ws://localhost:5000");
    ws.onopen = function(evt)
    {
        gui.serverMessage("Connected to server.");
    };

    ws.onerror = function(err)
    {
        gui.serverMessage("Could not connect to server.");
    };
     
    ws.onmessage = function (evt) 
    { 
       update(JSON.parse(evt.data));
    };
     
    ws.onclose = function(evt)
    { 
        gui.serverMessage("Connection to server lost. <a href='#' onclick='javascript:connect_to_server()'>Reconnect</a>.");
    };
};


