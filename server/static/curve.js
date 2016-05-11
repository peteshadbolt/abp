// Curve settings
var curveProperties = {
    splineDensity: 10,
    curvature: 100
};

// Add a curved edge between two points
function makeEdge(start, end) {
    // Make the geometry of the curve
    var a = new THREE.Vector3(start.x, start.y, start.z);
    var b = new THREE.Vector3(end.x, end.y, end.z);
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

