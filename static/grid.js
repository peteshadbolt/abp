
// Make a grid
function makeGrid(side, n, color) {
    var markers = new THREE.Object3D();
    var gridStyle = {
        color: color,
        transparent: true,
        linewidth: 1,
        opacity: 0.5
    };
    var material = new THREE.LineBasicMaterial(gridStyle);
    for (var i = -n / 2; i <= n / 2; ++i) {
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(side * i / n, -side / 2, 0));
        geometry.vertices.push(new THREE.Vector3(side * i / n, side / 2, 0));
        var line = new THREE.Line(geometry, material);
        var line90 = line.clone();
        line90.rotation.z = Math.PI / 2;
        markers.add(line);
        markers.add(line90);
    }
    return markers;
}
