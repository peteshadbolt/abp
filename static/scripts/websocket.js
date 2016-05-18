define(["message"], function(message){
return {
    bindEvents: function(update){
        var ws = new WebSocket("ws://localhost:5000");
        ws.onopen = function(evt)
        {
            message.innerHTML = "Connected to server.";
            message.className = "visible";
        };

        ws.onerror = function(err)
        {
            message.innerHTML = "Could not connect to server.";
            message.className = "visible";
        };
         
        ws.onmessage = function (evt) 
        { 
           console.log("Received update");
           update(JSON.parse(evt.data));
        };
         
        ws.onclose = function(evt)
        { 
            message.innerHTML = "Connection to server lost. <a href='#' onclick='javascript:connect_to_server()'>Reconnect</a>.";
            message.className = "visible";
        };
    }
    };
}
);


