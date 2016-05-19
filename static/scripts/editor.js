var editor = {};
editor.nearest = undefined;
editor.gimbalVertices = [];

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
    //if (n.type=="node") {
        var p = abj.meta[n].position;
        editor.gimbal.position.set(p.x, p.y, p.z);
        gui.controls.target.set(p.x, p.y, p.z);
        gui.hideNodeMessage();
        editor.nearest = undefined;
        gui.render();
    //}
};

editor.prepare = function() {
    mouse.onFreeMove = editor.onFreeMove;
    mouse.onClick = editor.onClick;
    editor.makeGimbal();
};

// Gets a reference to the node nearest to the mouse cursor
editor.nearestNode = function(ray) {
    for (var i=0; i < editor.gimbalVertices.length; ++i) {
        if (ray.distanceSqToPoint(editor.gimbalVertices[i]) < 0.03) {
            //return {type: "gimbal", node: i};
        }
    }

    for (var j in abj.meta) {
        if (ray.distanceSqToPoint(abj.meta[j].position) < 0.03) {
            //return {type: "node", node: i};
            return j;
        }
    }
    return undefined;
};

editor.makeGimbal = function(center) {
    editor.gimbal = new THREE.Object3D();

    var pointGeometry = new THREE.Geometry();
    pointGeometry.vertices = [
        new THREE.Vector3(1, 0, 0),
        new THREE.Vector3(0, 1, 0),
        new THREE.Vector3(0, 0, 1),
        new THREE.Vector3(-1, 0, 0),
        new THREE.Vector3(0, -1, 0),
        new THREE.Vector3(0, 0, -1)
    ];
    editor.gimbalVertices = pointGeometry.vertices;
    var tips = new THREE.Points(pointGeometry, materials.tip);

    editor.gimbal.add(tips);
    gui.scene.add(editor.gimbal);
};

