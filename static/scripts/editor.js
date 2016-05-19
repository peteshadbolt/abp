var editor = {};
var pi2 = Math.PI / 2;

editor.selection = undefined;

editor.orientations = [
    new THREE.Euler(pi2, 0, 0),
    new THREE.Euler(0, 0, 0),
    new THREE.Euler(pi2, 0, pi2),
];


editor.onFreeMove = function() {
    var found = editor.findNodeOnRay(mouse.ray);
    if (editor.selection !== found) {
        editor.selection = found;
        if (found) {
            gui.nodeMessage("Node " + found + " (VOP:" + abj.node[found].vop + ")" +
                "<br/>" + "Click to edit neighbourhood");
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

    abj.add_node(abj.order(), { position: point });
    editor.grid.position.copy(point);
    gui.controls.target.copy(point);
    graph.update();
    gui.serverMessage("Created node.");
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

editor.prepare = function() {
    mouse.onFreeMove = editor.onFreeMove;
    mouse.onClick = editor.onClick;
    document.addEventListener("keydown", editor.onKey, false);
    editor.makeGrid();
};

editor.onKey = function(evt) {
    if (evt.keyCode !== 32) {return;}
    editor.setOrientation((editor.orientation + 1) % 3);
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
