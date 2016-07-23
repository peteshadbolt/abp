var materials = {};

var curveProperties = {
    splineDensity: 1,
    curvature: 20
};

// Is called on boot
materials.prepare = function() {
    var ballSprite = new THREE.Texture(document.getElementById("ball"));
    ballSprite.needsUpdate = true;
    materials.edge = new THREE.LineBasicMaterial({
        color: "gray",
        transparent: false,
        linewidth: 2
    });
    materials.qubit = new THREE.PointsMaterial({
        size: 0.3,
        map: ballSprite,
        alphaTest: 0.5,
        transparent: true,
        vertexColors: THREE.VertexColors
    });
};

materials.makeCurve = function(a, b) {
    var length = new THREE.Vector3().subVectors(a, b).length();
    var bend = new THREE.Vector3(length / curveProperties.curvature, length / curveProperties.curvature, 0);
    var mid = new THREE.Vector3().add(a).add(b).multiplyScalar(0.5).add(bend);
    var spline = new THREE.CatmullRomCurve3([a, mid, b]);
    var geometry = new THREE.Geometry();
    var splinePoints = spline.getPoints(curveProperties.splineDensity);
    Array.prototype.push.apply(geometry.vertices, splinePoints);
    return new THREE.Line(geometry, materials.edge);
};

