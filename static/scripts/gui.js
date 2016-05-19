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
    gui.camera.position.set(0, 0, 10);
};

// Someone resized the window
gui.onWindowResize = function(evt) {
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
};

// Put an HTML message to the screen
// TODO: write a generic messaging class?
gui.serverMessage = function(msgtext, persist) {
    if (persist === undefined) {persist = false;}
    server_info.innerHTML = msgtext;
    server_info.className = "visible";
    clearInterval(gui.ki);
    if (!persist){
        gui.ki = setInterval(function(){server_info.className="hidden";}, 3000);
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
    editor.update();
    requestAnimationFrame(gui.loop);
};

