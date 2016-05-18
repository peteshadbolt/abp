var mouse = {};
var interaction = {};

interaction.raycaster = new THREE.Raycaster();
interaction.xyplane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);

// Gets a reference to the node nearest to the mouse cursor
interaction.nearestNode = function() {
    this.raycaster.setFromCamera(mouse, camera);
    for (var i = 0; i < nodeGeometry.vertices.length; ++i) {
        var v = nodeGeometry.vertices[i];
        if (this.raycaster.ray.distanceSqToPoint(v) < 0.01) {
            return i;
        }
    }
    return undefined;
};


// Find out: what is the mouse pointing at?
interaction.checkIntersections = function() {
    var new_selection = nearestNode();
    if (new_selection != this.selection) {
        this.selection = new_selection;
        info.className = this.selection ? "visible" : "hidden";
        info.innerHTML = this.selection ? nodeGeometry.labels[new_selection] : info.innerHTML;
        render();
    }
};

// Update the mouse position tracker
interaction.onMouseMove = function(event) {
    mouse.wasClick = false;
    mouse.absx = event.clientX;
    mouse.absy = event.clientY;
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    //w = 200; //h = 15; //info.style.top = mouse.absy - h - 40 + "px"; //info.style.left = mouse.absx - w / 2 + "px"; //checkIntersections();
};

// Try to add a qubit at the current mouse position
interaction.addQubitAtMouse = function(event) {
    this.raycaster.setFromCamera(mouse, camera);
    var intersection = this.raycaster.ray.intersectPlane(this.plane);
    intersection.x = Math.round(intersection.x);
    intersection.y = Math.round(intersection.y);
    abj.add_node(Object.keys(vops).length, {
        "position": intersection
    });
    updateScene();
}

interaction.bind = function() {
    var el = renderer.domElement;
    el.addEventListener("mousedown", this.onMouseDown);
    el.addEventListener("mouseup", this.onMouseDown);
    el.addEventListener("mousemove", this.onMouseMove);
};
