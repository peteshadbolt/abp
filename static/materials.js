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
        color: 0xcccccc,
        size: 0.1,
        map: textures.sprite,
        alphaTest: 0.5,
        transparent: true,
    };
    materials.point = new THREE.PointsMaterial(pointStyle);

    var qubitStyle = {
        size: 0.6,
        map: textures.sprite,
        alphaTest: 0.5,
        transparent: true,
        color: "red"
    };

    materials.qubit = new THREE.PointsMaterial(qubitStyle);
}
