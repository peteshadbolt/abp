var graph = {};
graph.colors = ["red", "green", "yellow", "blue", "pink", "orange", "purple"];

graph.hook = function() {
    materials.load();
    websocket.connect(graph.update);
};

graph.update = function(json) {
    abj.vops = json.vops;
    abj.ngbh = json.ngbh;
    abj.meta = json.meta;
    graph.updateScene();
};

graph.updateScene = function() {
    if (graph.object){gui.scene.remove(graph.object);}
    graph.object = null;
    console.log("update");

    var geometry = new THREE.Geometry();
    geometry.colors = [];
    for (var i in abj.vops) {
        var vop = abj.vops[i];
        var pos = abj.meta[i].position;
        var vertex = new THREE.Vector3(pos.x, pos.y, pos.z);
        geometry.vertices.push(vertex);
        geometry.colors.push(new THREE.Color(graph.colors[abj.vops[i] % graph.colors.length]));
    }

    var edges = new THREE.Object3D();
    var my_edges = abj.edgelist();
    for (i = 0; i < my_edges.length; ++i) {
        var edge = my_edges[i];
        var start = abj.meta[edge[0]].position;
        var startpos = new THREE.Vector3(start.x, start.y, start.z);
        var end = abj.meta[edge[1]].position;
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
