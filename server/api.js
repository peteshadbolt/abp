var ws;

function connect_to_server() {
    ws = new WebSocket("ws://localhost:5001");
    ws.onopen = function()
    {
       console.log("Connected to server.");
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
       console.log("Connection was closed.");
    };
}


