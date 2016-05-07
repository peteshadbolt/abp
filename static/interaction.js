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

// Update the mouse position tracker
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

// Add qubits or whatever
function onClick(event){
    if (!selection){return;}
    console.log(nodeGeometry.vertices[selection]);
    qubits.geometry.dynamic = true;
    qubits.geometry.vertices.push(nodeGeometry.vertices[selection].clone());
    qubits.geometry.verticesNeedUpdate = true;
}

