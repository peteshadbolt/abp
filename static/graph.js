var colors = ["red", "green", "yellow", "blue", "pink", "orange", "purple"];

function updateScene() {
    var oldState = scene.getObjectByName("graphstate");
    scene.remove(oldState);
    oldState = null;
   
    var geometry = new THREE.Geometry();
    for (var i in abj.vops) {
        var vop = abj.vops[i];
        var pos = abj.meta[i].position;
        var vertex = new THREE.Vector3(pos.x, pos.y, pos.z);
        geometry.vertices.push(vertex);
        geometry.colors[i] = new THREE.Color(colors[abj.vops[i] % colors.length]);
    }

    var edges = new THREE.Object3D();
    var my_edges = abj.edgelist();
    for (i=0; i < my_edges.length; ++i) {
        var edge = my_edges[i];
        var start = abj.meta[edge[0]].position;
        var startpos = new THREE.Vector3(start[0], start[1], start[2]);
        var end = abj.meta[edge[1]].position;
        var endpos = new THREE.Vector3(end[0], end[1], end[2]);
        var newEdge = makeEdge(startpos, endpos);
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

