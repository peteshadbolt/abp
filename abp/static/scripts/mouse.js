var mouse = {};
mouse.wasClick = true;
mouse.pressed = false;

mouse.raycaster = new THREE.Raycaster();

mouse.onFreeMove = function() {
    console.log("Free move");
};
mouse.onDrag = function() {
    //console.log("Drag");
};
mouse.onClick = function() {
    console.log("Click");
};
mouse.onCtrlClick = function() {
    console.log("Ctrl-click");
};
mouse.onShiftClick = function() {
    console.log("Shift-click");
};

mouse.prepare = function() {
    var el = gui.renderer.domElement;
    el.addEventListener("mousedown", mouse.onDown);
    el.addEventListener("mouseup", mouse.onUp);
    el.addEventListener("mousemove", mouse.onMove);
};

mouse.onDown = function(event) {
    mouse.wasClick = true;
    mouse.pressed = true;
};

mouse.onUp = function(event) {
    mouse.pressed = false;
    if (!mouse.wasClick) {
        return;
    }
    if (event.ctrlKey) {
        mouse.onCtrlClick();
    } else if (event.shiftKey) {
        mouse.onShiftClick();
    } else {
        mouse.onClick();
    }
};

mouse.onMove = function(event) {
    // TODO: wasclick sux
    mouse.wasClick = false;
    mouse.position_absolute = {
        x: event.clientX,
        y: event.clientY
    };
    mouse.position_relative = {
        x: (event.clientX / window.innerWidth) * 2 - 1,
        y: -(event.clientY / window.innerHeight) * 2 + 1
    };
    gui.setInfoPosition(mouse.position_absolute);
    mouse.raycaster.setFromCamera(mouse.position_relative, gui.camera);
    mouse.ray = mouse.raycaster.ray;
    if (mouse.pressed) {
        mouse.onDrag();
    } else {
        mouse.onFreeMove();
    }
};
