function buildGraph(json) {
    // Add all the qubits
    var geometry = new THREE.Geometry();
    var vertex = new THREE.Vector3(0, 0, 0);
    geometry.vertices.push(vertex);
    var nodes = new THREE.Points(geometry, materials.node);

    // Add all the edges
    var edges = new THREE.Object3D();
    edges.add(makeEdge({
        "start": [0, 0, 0],
        "end": [1, 1, 1]
    }));
    
    // Construct and return
    var graph = new THREE.Object3D();
    graph.add(nodes);
    graph.add(edges);
    return graph;
}
