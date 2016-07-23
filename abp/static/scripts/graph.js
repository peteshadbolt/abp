var graph = {};
graph.colors = ["red", "green", "yellow", "green", "pink", "orange", "purple"];

graph.prepare = function() {
    materials.prepare();
    websocket.connect(graph.update);
};

graph.center = function() {
    var middle = new THREE.Vector3(0, 0, 0);
    for (var i in abj.node) {
        middle = middle.add(abj.node[i].position);
    }
    middle = middle.multiplyScalar(1.0/abj.order());
    return middle;
};

graph.update = function(newState) {
    if (newState){abj.update(newState);}

    var gs = gui.scene.getObjectByName("graphstate");
    if (gs){ gui.scene.remove(gs); }

    var geometry = new THREE.Geometry();
    geometry.colors = [];
    for (var i in abj.node) {
        var color = graph.colors[abj.node[i].vop % graph.colors.length];
        if (abj.node[i].color !== undefined){
            color = abj.node[i].color;
        }
        geometry.vertices.push(abj.node[i].position);
        geometry.colors.push(new THREE.Color(color));
    }

    graph.center();
    gui.controls.target.copy(graph.center());

    var edges = new THREE.Object3D();
    var my_edges = abj.edgelist();
    for (i = 0; i < my_edges.length; ++i) {
        var edge = my_edges[i];
        var start = abj.node[edge[0]].position;
        var startpos = new THREE.Vector3(start.x, start.y, start.z);
        var end = abj.node[edge[1]].position;
        var endpos = new THREE.Vector3(end.x, end.y, end.z);
        var newEdge = materials.makeCurve(startpos, endpos);
        edges.add(newEdge);
    }

    var particles = new THREE.Points(geometry, materials.qubit);
    var object = new THREE.Object3D();
    object.name = "graphstate";
    object.add(particles);
    object.add(edges);
    gui.scene.add(object);
    gui.render();
};

