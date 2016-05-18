var textures = {};
var materials = {};

// Load the site texture from the data URI
function loadMaterials(argument) {
    textures.sprite = new THREE.Texture(document.getElementById("ball"));
    textures.sprite.needsUpdate = true;

    var lineStyle = {
        color: "gray",
        transparent: false,
        linewidth: 1
    };
    materials.edge = new THREE.LineBasicMaterial(lineStyle);

    var pointStyle = {
        size: 0.1,
        map: textures.sprite,
        alphaTest: 0.5,
        transparent: true,
        vertexColors:THREE.VertexColors
    };
    materials.point = new THREE.PointsMaterial(pointStyle);

    var qubitStyle = {
        size: 0.8,
        map: textures.sprite,
        alphaTest: 0.5,
        transparent: true,
        vertexColors:THREE.VertexColors
    };

    materials.qubit = new THREE.PointsMaterial(qubitStyle);
}

// Curve settings
var curveProperties = {
    splineDensity: 10,
    curvature: 100
};

// Add a curved edge between two points
function makeCurve(a, b) {
    // Make the geometry of the curve
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

