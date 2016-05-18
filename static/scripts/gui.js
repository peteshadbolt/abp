var gui = {};
gui.prepare = function() {
    gui.renderer = new THREE.WebGLRenderer({
        "antialias": true
    });
    gui.renderer.setSize(window.innerWidth, window.innerHeight);
    gui.renderer.setClearColor(0xffffff, 1);
    document.querySelector("body").appendChild(gui.renderer.domElement);
    window.addEventListener("resize", gui.onWindowResize, false);

    gui.makeScene();

    gui.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.3, 1000);
    gui.controls = new THREE.OrbitControls(gui.camera);
    gui.controls.addEventListener("change", gui.render);
    gui.controls.center.set(0, 0, 0);
    gui.controls.target.set(0, 0, 0);
    gui.controls.rotateSpeed = 0.2;
    gui.controls.userPanSpeed = 0.1;
    gui.camera.position.set(4, 4, 10);
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
    requestAnimationFrame(function() {
        gui.renderer.render(gui.scene, gui.camera);
    });
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
gui.serverMessage = function(msgtext) {
    if (msgtext) {
        server_info.innerHTML = msgtext;
        server_info.className = "visible";
    } else {
        server_info.innerHTML = "";
        server_info.className = "hidden";
    }
};

gui.nodeMessage = function(msgtext) {
    node_info.innerHTML = msgtext;
    node_info.className = "visible";
};

gui.hideNodeMessage = function(){
    node_info.className = "hidden";
};

// Set the position of the info popup
gui.setInfoPosition = function(position){
    w = node_info.offsetWidth; 
    h = node_info.offsetHeight;
    node_info.style.left = position.x -  w/2 + "px"; 
    node_info.style.top = position.y - h -10 + "px"; 
};

// The main loop
gui.loop = function() {
    gui.controls.update();
    requestAnimationFrame(gui.loop);
};

// Try to add a qubit at the current mouse position
gui.addQubitAtMouse = function(event) {
    this.raycaster.setFromCamera(mouse, camera);
    var intersection = this.raycaster.ray.intersectPlane(this.plane);
    intersection.x = Math.round(intersection.x);
    intersection.y = Math.round(intersection.y);
    abj.add_node(Object.keys(vops).length, {
        "position": intersection
    });
    graph.update();
};

