
function poll() {
    var ws = new WebSocket("ws://localhost:5000/echo");
    ws.onopen = function()
    {
       // Web Socket is connected, send data using send()
       ws.send("Hello from the browser! I connected okay");
       console.log("Sent a message to the server");
    };
     
    ws.onmessage = function (evt) 
    { 
       var received_msg = evt.data;
       console.log("I got a message from the server:");
       console.log(evt.data);
    };
     
    ws.onclose = function()
    { 
       ws.send("Bye by from the browser");
       console.log("Connection is closed..."); 
    };
}

function updateScene(state) {
    if (state.needs_update === false){return;}
    var oldState = scene.getObjectByName("graphstate");
    scene.remove(oldState);
    oldState = null;
   
    var geometry = new THREE.Geometry();
    //nodeGeometry.labels = [];
    //nodeGeometry.colors = [];
    for (var i in state.nodes) {
        var node = state.nodes[i];
        var pos = state.meta[i].pos;
        var vertex = new THREE.Vector3(pos.x, pos.y, pos.z);
        geometry.vertices.push(vertex);
        //geometry.colors[i] = new THREE.Color(n.color);
        //geometry.labels[i] = n.label;
    }

    var edges = new THREE.Object3D();
    for (i=0; i < state.edges.length; ++i) {
        var edge = state.edges[i];
        var start = state.meta[edge[0]].pos;
        var end = state.meta[edge[1]].pos;
        var newEdge = makeEdge(start, end);
        edges.add(newEdge);
    }

    var particles = new THREE.Points(geometry, materials.qubit);
    var newState = new THREE.Object3D();
    newState.name = "graphstate";
    newState.add(particles);
    newState.add(edges);
    scene.add(newState);
    render();
}
