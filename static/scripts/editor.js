var editor = {};
var pi2 = Math.PI / 2;

editor.nearest = undefined;

editor.orientations = [
    new THREE.Matrix4(),
    new THREE.Matrix4(),
    new THREE.Matrix4()
];

editor.orientation = 0;

editor.orientations[1].makeRotationX(pi2);
editor.orientations[2].makeRotationX(pi2);
editor.orientations[2].makeRotationZ(pi2);

editor.onFreeMove = function() {
    var n = editor.nearestNode(mouse.ray);
    if (editor.nearest !== n) {
        editor.nearest = n;
        if (n) {
            gui.nodeMessage("Node " + n + " (VOP:" + abj.vops[n] + ")" +
                "<br/>" + "Click to edit neighbourhood");
        } else {
            gui.hideNodeMessage();
        }
    }
};

editor.onClick = function() {
    var n = editor.nearestNode(mouse.ray);
    if (n) {
        var p = abj.meta[n].position;
        editor.grid.position.set(p.x, p.y, p.z);
        gui.controls.target.set(p.x, p.y, p.z);
        gui.hideNodeMessage();
        editor.nearest = undefined;
        gui.serverMessage("Selected node " + n + "");
    } else {
        //TODO: ghastly
        var intersection = mouse.ray.intersectPlane(editor.plane);
        intersection.x = Math.round(intersection.x, 0);
        intersection.y = Math.round(intersection.y, 0);
        intersection.z = Math.round(intersection.z, 0);
        var newNode = abj.order();
        abj.add_node(newNode, {
            position: intersection
        });
        editor.grid.position.set(intersection.x, intersection.y, intersection.z);
        gui.controls.target.set(intersection.x, intersection.y, intersection.z);
        graph.update();
        gui.serverMessage("Created node " + newNode + " at ");
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
        editor.orientation = (editor.orientation+1) % 3;
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
    editor.grid.matrixAutoUpdate = false;
    editor.plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    gui.scene.add(editor.grid);
};

editor.update = function(){
};

// Gets a reference to the node nearest to the mouse cursor
// TODO: get rid of meta{}
editor.nearestNode = function(ray) {
    for (var j in abj.meta) {
        if (ray.distanceSqToPoint(abj.meta[j].position) < 0.03) {
            return j;
        }
    }
    return undefined;
};
