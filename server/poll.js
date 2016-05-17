function poll() {
    var ws = new WebSocket("ws://localhost:5001");
    ws.onopen = function()
    {
       console.log("Connected to server.");
    };
     
    ws.onmessage = function (evt) 
    { 
       var received_msg = evt.data;
       console.log("Message received: " + evt.data);
    };
     
    ws.onclose = function()
    { 
       console.log("Connection was closed.");
    };
}

window.onload = poll;

