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
