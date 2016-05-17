var ws;

function connect_to_server() {
    ws = new WebSocket("ws://localhost:5000");
    ws.onopen = function()
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
       var new_state = JSON.parse(evt.data);
       vops = new_state.vops;
       ngbh = new_state.ngbh;
       meta = new_state.meta;
       updateScene();
    };
     
    ws.onclose = function()
    { 
        message.innerHTML = "Connection to server lost. <a href='#' onclick='javascript:connect_to_server()'>Reconnect</a>.";
        message.className = "visible";
    };
}


