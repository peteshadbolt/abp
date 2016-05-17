var controls, renderer, raycaster, scene, selection, camera;

var mouseprevpos = {};

// Run on startup
window.onload = init;

// Clear the whole scene
function makeScene() {
    var myScene = new THREE.Scene();
    var grid = new THREE.GridHelper(20, 2);
    grid.rotation.x = Math.PI/2;
    grid.setColors(0xdddddd, 0xeeeeee);
    myScene.add(grid);
    return myScene;
}


// Render the current frame to the screen
function render() {
    requestAnimationFrame(function () {
        renderer.render(scene, camera);
    });
}

// Someone resized the window
function onWindowResize(evt){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

function bind_events() {
    window.addEventListener("resize", onWindowResize, false);
    renderer.domElement.addEventListener("mousedown", function (event) {
        var mouse = new THREE.Vector2(); // create once and reuse
        mouse.x = ( event.clientX / renderer.domElement.width ) * 2 - 1;
        mouse.y = - ( event.clientY / renderer.domElement.height ) * 2 + 1;
        mouseprevpos.x = mouse.x;
        mouseprevpos.y = mouse.y;
    });

    renderer.domElement.addEventListener("mouseup", function (event) {
        var mouse = new THREE.Vector2(); // create once and reuse
        mouse.x = ( event.clientX / renderer.domElement.width ) * 2 - 1;
        mouse.y = - ( event.clientY / renderer.domElement.height ) * 2 + 1;
        if (mouse.x != mouseprevpos.x || mouse.y != mouseprevpos.y ){return;}

        var raycaster = new THREE.Raycaster(); // create once and reuse
        raycaster.setFromCamera( mouse, camera );
        var plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
        var intersection = raycaster.ray.intersectPlane(plane);
        console.log(intersection);

        intersection.x = Math.round(intersection.x);
        intersection.y = Math.round(intersection.y);
        add_node(Object.keys(vops).length, intersection);
        updateScene();
    });
    controls.addEventListener("change", render);

}


// Called on startup
function init() {
    // Renderer
    renderer = new THREE.WebGLRenderer({"antialias":true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(renderer.domElement);

    // Time to load the materials
    loadMaterials();

    // Camera, controls, raycaster
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.3, 100);
    controls = new THREE.OrbitControls(camera);

    // Center the camera
    // TODO: frustrum
    controls.center.set(0, 0, 0);
    controls.rotateSpeed = 0.2;
    camera.position.set(0, 0, 40);

    // Run
    bind_events();
    scene = makeScene();
    connect_to_server();
    render();
}
