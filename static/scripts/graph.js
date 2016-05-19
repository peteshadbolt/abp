var graph = {};
graph.colors = ["lightblue", "green", "yellow", "red", "pink", "orange", "purple"];

graph.prepare = function() {
    materials.prepare();
    websocket.connect(graph.update);
};

graph.update = function(newState) {
    if (newState){abj.update(newState);}

    if (graph.object){gui.scene.remove(graph.object);}
    graph.object = null;

    var geometry = new THREE.Geometry();
    geometry.colors = [];
    for (var i in abj.node) {
        var color = graph.colors[abj.node[i].vop % graph.colors.length];
        geometry.vertices.push(abj.node[i].position);
        geometry.colors.push(new THREE.Color(color));
    }

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
    graph.object = new THREE.Object3D();
    graph.object.name = "graphstate";
    graph.object.add(particles);
    graph.object.add(edges);
    gui.scene.add(graph.object);
    gui.render();
};

