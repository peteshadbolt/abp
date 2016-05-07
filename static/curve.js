// Curve settings
var curveProperties = {
    splineDensity: 30,
    curvature: 10
};

// Add a curved edge between two points
function makeEdge(e) {
    // Make the geometry of the curve
    var a = new THREE.Vector3(e.start[0], e.start[1], e.start[2]);
    var b = new THREE.Vector3(e.end[0], e.end[1], e.end[2]);
    var length = new THREE.Vector3().subVectors(a, b).length();
    var bend = new THREE.Vector3(length / curveProperties.curvature, length / curveProperties.curvature, 0);
    var mid = new THREE.Vector3().add(a).add(b).multiplyScalar(0.5).add(bend);
    var spline = new THREE.CatmullRomCurve3([a, mid, b]);
    var geometry = new THREE.Geometry();
    var splinePoints = spline.getPoints(curveProperties.splineDensity);
    Array.prototype.push.apply(geometry.vertices, splinePoints);

    // Make the actual Object3d thing
    var line = new THREE.Line(geometry, materials.edge);
    return line;
}

