var controls, renderer, raycaster, scene, selection, camera;

var mouseprevpos = {};

// Run on startup
window.onload = init;


// Clear the whole scene
function makeScene() {
    var myScene = new THREE.Scene();
    var grid = new THREE.GridHelper(10, 1);
    grid.rotation.x = Math.PI / 2;
    grid.setColors(0xdddddd, 0xeeeeee);
    myScene.add(grid);
    return myScene;
}


// Render the current frame to the screen
function render() {
    requestAnimationFrame(function() {
        renderer.render(scene, camera);
    });
}

// Someone resized the window
function onWindowResize(evt) {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}


// Called on startup
function init() {
    // Renderer
    renderer = new THREE.WebGLRenderer({
        "antialias": true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(renderer.domElement);
    window.addEventListener("resize", onWindowResize, false);

    // Time to load the materials
    loadMaterials();

    // Camera, controls, raycaster
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.3, 1000);
    controls = new THREE.OrbitControls(camera);
    controls.center.set(0, 0, 0);
    controls.rotateSpeed = 0.2;
    camera.position.set(0, 0, 20);
    controls.addEventListener("change", render);

    // Run
    scene = makeScene();
    connectToServer();
    render();
}
