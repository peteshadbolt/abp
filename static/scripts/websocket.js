define(["message"], function(message){
return {
    connect: function(update){
        var ws = new WebSocket("ws://localhost:5000");
        ws.onopen = function(evt)
        {
            message.serverMessage("Connected to server.");
        };

        ws.onerror = function(err)
        {
            message.serverMessage("Could not connect to server.");
        };
         
        ws.onmessage = function (evt) 
        { 
           update(JSON.parse(evt.data));
        };
         
        ws.onclose = function(evt)
        { 
            message.serverMessage("Connection to server lost. <a href='#' onclick='javascript:connect_to_server()'>Reconnect</a>.");
        };
    }
    };
}
);


