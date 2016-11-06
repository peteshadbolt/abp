var editor = {};
var pi2 = Math.PI / 2;

editor.selection = undefined;
editor.mouseOver = undefined;

editor.orientations = [
    new THREE.Euler(pi2, 0, 0),
    new THREE.Euler(0, 0, 0),
    new THREE.Euler(pi2, 0, pi2),
];


editor.onFreeMove = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (editor.mouseOver !== found) {
        editor.mouseOver = found;
        if (found) {
            var n = abj.node[found];
            var s = "Node " + found + "<br/> ";
            for (var i in n) {
                if (i!="position"){
                    s += i + ":" + n[i] + " ";
                }
            }
            s += "";
            gui.nodeMessage(s);
        } else {
            gui.hideNodeMessage();
        }
    }
};

editor.focus = function(node) {
    gui.hideNodeMessage();
    editor.selection = node;

    //gui.serverMessage("Selected node " + node + ".");
};

editor.addQubitAtPoint = function(point) {
    if (point === null) {
        return;
    }
    point.round();
    var new_node = Math.floor(point.x) + "," + Math.floor(point.y) + "," + Math.floor(point.z);
    if (Object.prototype.hasOwnProperty.call(abj.node, new_node)) {
        gui.serverMessage("Node " + new_node +" already exists.");
        return;
    }
    websocket.edit({action:"create", name:new_node, position: point});
    editor.focus(new_node);
    gui.serverMessage("Created node " + new_node +".");
};

editor.onClick = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (found) {
        editor.focus(found);
        var node=found;
        editor.grid.position.copy(abj.node[node].position);
        gui.controls.target.copy(abj.node[node].position);
        node_name.innerHTML = "Node " + node;
        node_data.className = "visible";
        node_vop.innerHTML = "VOP: " + abj.node[node].vop;
    } else {
        var intersection = mouse.ray.intersectPlane(editor.plane);
        if (intersection !== null) {
            editor.addQubitAtPoint(intersection);
        }
    }
};

editor.onShiftClick = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (found === undefined){ return; }
    if (editor.selection === undefined){ return; }
    if (found === editor.selection){ return; }
    //abj.act_cz(found, editor.selection);
    websocket.edit({action:"cz", start:found, end:editor.selection});
    gui.serverMessage("Acted CZ between " + found + " & " + editor.selection + ".");
    editor.focus(found);
};

editor.onCtrlClick = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (found === undefined){ return; }
    if (editor.selection === undefined){ return; }
    editor.focus(found);
    websocket.edit({action:"hadamard", node:found});
    gui.serverMessage("Acted H on node " + found + ".");
};


editor.prepare = function() {
    mouse.onFreeMove = editor.onFreeMove;
    mouse.onClick = editor.onClick;
    mouse.onShiftClick = editor.onShiftClick;
    mouse.onCtrlClick = editor.onCtrlClick;
    document.addEventListener("keydown", editor.onKey, false);
    editor.makeGrid();
};

editor.onKey = function(evt) {
    if (evt.keyCode === 32) {
        editor.setOrientation((editor.orientation + 1) % 3);
    }
    if (evt.keyCode === 46 || evt.keyCode === 68) {
        editor.deleteNode();
    }
};

editor.setOrientation = function(orientation) {
    editor.orientation = orientation;
    var rotation = editor.orientations[orientation];
    var normal = new THREE.Vector3(0, 1, 0);
    normal.applyEuler(rotation);
    editor.grid.rotation.copy(rotation);
    editor.plane = new THREE.Plane();
    editor.plane.setFromNormalAndCoplanarPoint(normal, editor.grid.position);
    gui.render();
};

editor.makeGrid = function() {
    editor.grid = new THREE.GridHelper(10, 1);
    editor.grid.setColors(0xbbbbbb, 0xeeeeee);
    editor.setOrientation(0);
    gui.scene.add(editor.grid);
};

editor.update = function() {};

// Gets a reference to the node nearest to the mouse cursor
editor.findNodeOnRay = function(ray) {
    for (var n in abj.node) {
        if (ray.distanceSqToPoint(abj.node[n].position) < 0.012) {
            return n;
        }
    }
    return undefined;
};

editor.deleteNode = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"delete", node:editor.selection});
    gui.serverMessage("Deleted node " + editor.selection + ".");
    editor.selection = undefined;
    node_data.className = "hidden";
};

//TODO: loadsa space for DRY here

editor.hadamard = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"hadamard", node:editor.selection});
    gui.serverMessage("Acted Hadamard on node " + editor.selection + ".");
};

editor.phase = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"phase", node:editor.selection});
    gui.serverMessage("Acted phase on node " + editor.selection + ".");
};

editor.measureX = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"measure", node:editor.selection, basis:"x"});
    gui.serverMessage("Measured node " + editor.selection + " in X.");
};

editor.measureY = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"measure", node:editor.selection, basis:"y"});
    gui.serverMessage("Measured node " + editor.selection + " in Y.");
};

editor.measureZ = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"measure", node:editor.selection, basis:"z"});
    gui.serverMessage("Measured node " + editor.selection + " in z.");
};

editor.localComplementation = function() {
    if (editor.selection === undefined){ return; }
    websocket.edit({action:"localcomplementation", node:editor.selection});
    abj.local_complementation(editor.selection);
    gui.serverMessage("Inverted neighbourhood of " + editor.selection + ".");
};
