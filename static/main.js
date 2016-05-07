// IE9
if (typeof console === "undefined") {
    var console = {
        log: function(logMsg) {}
    };
}

var controls, renderer, raycaster, scene, info, nodeGeometry, selection;
var mouse = {
    "x": 0,
    "y": 0
};
var materials = {};
var curveProperties = {
    splineDensity: 30,
    curvature: 10
};
var camera;
var qubits;

// Run on startup
window.onload = init;

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

function makeQubits() {
    qubitGeometry = new THREE.Geometry();
    qubitGeometry.labels = [];
    var vertex = new THREE.Vector3(0, 0, 0);
    qubitGeometry.vertices.push(vertex);
    particles = new THREE.Points(qubitGeometry, materials.qubit);
    return particles;
}

// Clear the whole scene
function makeScene() {
    // Scene, controls, camera and so on
    var myScene = new THREE.Scene();

    // Materials
    var lineStyle = {
        color: "gray",
        transparent: false,
        linewidth: 1
    };
    materials.edge = new THREE.LineBasicMaterial(lineStyle);

    var pointStyle = {
        color: "0xcccccc",
        size: 0.1,
        map: materials.sprite,
        alphaTest: 0.5,
        transparent: true,
    };
    materials.point = new THREE.PointsMaterial(pointStyle);

    var qubitStyle = {
        size: 0.6,
        map: materials.sprite,
        alphaTest: 0.5,
        transparent: true,
        color: "red"
    };
    materials.qubit = new THREE.PointsMaterial(qubitStyle);

    // Build all the edges
    //var edgeGroup = new THREE.Object3D();

    qubits = makeQubits();
    myScene.add(qubits);

    // Build all the nodes
    nodeGeometry = new THREE.Geometry();
    nodeGeometry.labels = [];
    for (var i = 0; i < 10; ++i) {
        for (var j = 0; j < 10; ++j) {
            var vertex = new THREE.Vector3(i - 5, j - 5, 0);
            nodeGeometry.vertices.push(vertex);
            nodeGeometry.labels.push("Click to add a qubit at (" + i + ",  " + j + ")");
        }
    }

    var particles = new THREE.Points(nodeGeometry, materials.point);

    var grid = makeGrid(10, 10, "lightgray");
    myScene.add(grid);

    // Add the above stuff into the scene and return
    //myScene.add(edgeGroup);
    myScene.add(particles);
    return myScene;
}

// Gets a reference to the node nearest to the mouse cursor
function nearestNode() {
    raycaster.setFromCamera(mouse, camera);
    for (var i = 0; i < nodeGeometry.vertices.length; ++i) {
        if (raycaster.ray.distanceSqToPoint(nodeGeometry.vertices[i]) < 0.01) {
            return i;
        }
    }
    return undefined;
}

// Find out: what is the mouse pointing at?
function checkIntersections() {
    var new_selection = nearestNode();
    if (new_selection != selection) {
        selection = new_selection;
        info.className = selection ? "visible" : "hidden";
        info.innerHTML = selection ? nodeGeometry.labels[new_selection] : info.innerHTML;
        render();
    }
}

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
    for (var i = -n / 2; i < n / 2; ++i) {
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

// Handle mouse movement
function onMouseMove(event) {
    mouse.wasClick = false;
    mouse.absx = event.clientX;
    mouse.absy = event.clientY;
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    w = 200;
    h = 15;
    info.style.top = mouse.absy - h - 40 + "px";
    info.style.left = mouse.absx - w / 2 + "px";
    checkIntersections();
}

function onClick(event){
    if (!selection){return;}
    console.log(nodeGeometry.vertices[selection]);
    qubits.geometry.dynamic = true;
    qubits.geometry.vertices.push(nodeGeometry.vertices[selection].clone());
    qubits.geometry.verticesNeedUpdate = true;
}

// Render the current frame to the screen
function render() {
    renderer.render(scene, camera);
}

// This is the main control loop
function loopForever() {
    controls.update();
    requestAnimationFrame(loopForever);
}


// This just organises kickoff
function startMainLoop() {
    scene = makeScene();
    renderer.domElement.addEventListener("mousemove", onMouseMove, false);
    renderer.domElement.addEventListener("click", onClick, false);
    controls.addEventListener("change", render);
    loopForever();
}


// Called on startup
function init() {
    // Measure things, get references
    var width = window.innerWidth;
    var height = window.innerHeight;
    info = document.getElementById("infoholder");

    materials.sprite = new THREE.Texture(document.getElementById("ball"));
    materials.sprite.needsUpdate = true;

    // Renderer
    renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    renderer.setSize(width, height);
    renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(renderer.domElement);

    // Camera, controls, raycaster
    camera = new THREE.PerspectiveCamera(45, width / height, 0.3, 100);
    controls = new THREE.OrbitControls(camera);
    raycaster = new THREE.Raycaster();

    // Center the camera
    controls.center.set(0, 0, 0);
    controls.rotateSpeed = 0.2;
    camera.position.set(0, 0, 20);

    // Start polling
    setInterval(poll, 1000);

    // Run
    startMainLoop();
}
