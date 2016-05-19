var editor = {};
var pi2 = Math.PI / 2;

editor.selection = undefined;

editor.planes = [
    new THREE.Plane(new THREE.Vector3(0, 0, 1), 0),
    new THREE.Plane(new THREE.Vector3(0, 1, 0), 0),
    new THREE.Plane(new THREE.Vector3(1, 0, 0), 0)
];
editor.orientation = 0;
editor.plane = editor.planes[editor.orientation];

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
    gui.serverMessage("Selected node " + node + "");
};

editor.addQubitAtPoint = function(point) {
    if (point === null) {
        return;
    }
    point.round();
    abj.add_node(abj.order(), {
        position: point
    });
    editor.grid.position.copy(point);
    gui.controls.target.copy(point);
    graph.update();
    gui.serverMessage("Created node at " + JSON.stringify(point));
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
    if (evt.keyCode == 32) {
        editor.grid.rotation.x += Math.PI / 2;
        editor.orientation = (editor.orientation + 1) % 3;
        console.log(editor.orientation);
        var m = editor.orientations[editor.orientation];
        editor.plane.applyMatrix4(m);
        console.log(m);
        editor.grid.matrix = m;
        gui.render();
        gui.serverMessage("Rotated into the XY plane or whatever");
    }
};

editor.makeGrid = function() {
    editor.grid = new THREE.GridHelper(10, 1);
    editor.grid.rotation.x = Math.PI / 2;
    editor.grid.setColors(0xbbbbbb, 0xeeeeee);
    editor.grid.matrixAutoUpdate = true;
    gui.scene.add(editor.grid);
};

editor.update = function() {};

// Gets a reference to the node nearest to the mouse cursor
editor.findNodeOnRay = function(ray) {
    for (var n in abj.node) {
        if (ray.distanceSqToPoint(abj.node[n].position) < 0.03) {
            return n;
        }
    }
    return undefined;
};
