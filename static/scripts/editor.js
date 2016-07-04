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
    editor.grid.position.copy(abj.node[node].position);
    gui.controls.target.copy(abj.node[node].position);
    gui.hideNodeMessage();
    editor.selection = node;
    gui.serverMessage("Selected node " + node + ".");
    node_name.innerHTML = "Node " + node;
    node_data.className = "visible";
    node_vop.innerHTML = "VOP: " + abj.node[node].vop;
};

editor.addQubitAtPoint = function(point) {
    if (point === null) {
        return;
    }
    point.round();

    // Check for clashes
    for (var node in abj.node) {
        var delta = new THREE.Vector3();
        delta.subVectors(abj.node[node].position, point);
        if (delta.length()<0.1){ return; }
    }

    // TODO: This SUCKS
    var new_node = point.x + "." + point.y + "." + point.z;
    abj.add_node(new_node, { position: point, vop:0 });
    editor.focus(new_node);
    graph.update();
    gui.serverMessage("Created node " + new_node +".");
};

editor.onClick = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (found) {
        editor.focus(found);
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
    abj.act_cz(found, editor.selection);
    editor.focus(found);
    gui.serverMessage("Acted CZ between " + found + " & " + editor.selection + ".");
    graph.update();
};

editor.onCtrlClick = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (found === undefined){ return; }
    if (editor.selection === undefined){ return; }
    editor.focus(found);
    abj.act_hadamard(found);
    gui.serverMessage("Acted H on node " + found + ".");
    graph.update();
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
    abj.del_node(editor.selection);
    graph.update();
    gui.serverMessage("Deleted node " + editor.selection + ".");
    editor.selection = undefined;
    node_data.className = "hidden";
};

editor.localComplementation = function() {
    if (editor.selection === undefined){ return; }
    abj.local_complementation(editor.selection);
    graph.update();
    gui.serverMessage("Inverted neighbourhood of " + editor.selection + ".");
};
