var gui = {};
gui.construct = function() {
    gui.renderer = new THREE.WebGLRenderer();
    gui.renderer.setSize(window.innerWidth, window.innerHeight);
    gui.renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(gui.renderer.domElement);
    window.addEventListener("resize", gui.onWindowResize, false);

    gui.makeScene();

    gui.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.3, 1000);
    gui.controls = new THREE.OrbitControls(gui.camera);
    gui.controls.center.set(0, 0, 0);
    gui.controls.rotateSpeed = 0.2;
    gui.camera.position.set(0, 0, 20);
    gui.controls.addEventListener("change", gui.render);
};

// Someone resized the window
gui.onWindowResize = function(evt) {
    console.log(gui);
    gui.camera.aspect = window.innerWidth / window.innerHeight;
    gui.camera.updateProjectionMatrix();
    gui.renderer.setSize(window.innerWidth, window.innerHeight);
    gui.render();
};

// Render the current frame to the screen
gui.render = function() {
    console.log("render");
    gui.renderer.render(gui.scene, gui.camera);
};

// Make the extra bits of gui
gui.makeScene = function() {
    gui.scene = new THREE.Scene();
    var grid = new THREE.GridHelper(10, 1);
    grid.rotation.x = Math.PI / 2;
    grid.setColors(0xdddddd, 0xeeeeee);
    gui.scene.add(grid);
};

// Put an HTML message to the screen
gui.serverMessage = function(msgtext){
    message.innerHTML = msgtext;
    message.className = "visible";
};

