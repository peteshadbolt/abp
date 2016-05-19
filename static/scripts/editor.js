var editor = {};
editor.nearest = undefined;

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
    if (n){
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
        abj.add_node(newNode, {position:intersection});
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

editor.onKey = function(evt){
    if (evt.keyCode==32){
        editor.grid.rotation.x += Math.PI/2;
        var m = new THREE.Matrix4();
        m.makeRotationX(Math.PI/2);
        editor.plane.applyMatrix4(m);
        gui.render();
        gui.serverMessage("Rotated into the XY plane or whatever");
    }
};

editor.makeGrid = function() {
    editor.grid = new THREE.GridHelper(10, 1);
    editor.grid.rotation.x = Math.PI / 2;
    editor.grid.setColors(0xbbbbbb, 0xeeeeee);
    editor.plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    gui.scene.add(editor.grid);
}

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

