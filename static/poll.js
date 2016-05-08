var body;

function poll() {
    var xhr = new XMLHttpRequest();

    xhr.onload = function() {
        var state = JSON.parse(xhr.responseText);
        updateScene(state);
    };

    xhr.onerror = function(e){
        //soft_console.innerHTML = "\n" + "Lost connection to server";
    };

    xhr.open("GET", "/state", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}

function updateScene(state) {
    var oldState = scene.getObjectByName("graphstate");
    scene.remove(oldState);
    oldState = null;
   
    var geometry = new THREE.Geometry();
    //nodeGeometry.labels = [];
    //nodeGeometry.colors = [];
    for (var i in state.vops) {
        var vop = state.vops[i];
        var pos = state.meta[i].pos;
        var vertex = new THREE.Vector3(pos.x, pos.y, pos.z);
        geometry.vertices.push(vertex);
        //geometry.colors[i] = new THREE.Color(n.color);
        //geometry.labels[i] = n.label;
    }

    var edges = new THREE.Object3D();
    for (i=0; i < state.edge.length; ++i) {
        var edge = state.edge[i];
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
