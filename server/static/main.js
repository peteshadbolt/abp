// IE9
if (typeof console === "undefined") {
    var console = {
        log: function(logMsg) {}
    };
}

var controls, renderer, raycaster, scene, selection, camera;

// Run on startup
window.onload = init;

// Clear the whole scene
function makeScene() {
    var myScene = new THREE.Scene();
    var grid = makeGrid(10, 10, "lightgray");
    myScene.add(grid);
    return myScene;
}


// Render the current frame to the screen
function render() {
    requestAnimationFrame(function () {
        renderer.render(scene, camera);
    });
}

// This just organises kickoff
function startMainLoop() {
    scene = makeScene();
    controls.addEventListener("change", render);
    poll();
    render();
}

// Someone resized the window
function onWindowResize(evt){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}


// Called on startup
function init() {
    // Measure things, get references
    var width = window.innerWidth;
    var height = window.innerHeight;

    // Renderer
    renderer = new THREE.WebGLRenderer({"antialias":true});
    renderer.setSize(width, height);
    renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(renderer.domElement);
    window.addEventListener("resize", onWindowResize, false);

    // Time to load the materials
    loadMaterials();

    // Camera, controls, raycaster
    camera = new THREE.PerspectiveCamera(45, width / height, 0.3, 100);
    controls = new THREE.OrbitControls(camera);

    // Center the camera
    // TODO: frustrum
    controls.center.set(0, 0, 0);
    controls.rotateSpeed = 0.2;
    camera.position.set(0, 0, 40);

    // Start polling

    // Run
    startMainLoop();
}
