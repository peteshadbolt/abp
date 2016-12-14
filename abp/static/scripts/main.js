window.onload = function() {
    graph.prepare();
    materials.prepare();
    gui.prepare();
    mouse.prepare();
    editor.prepare();
    gui.scene.children[0].renderOrder = -1000;
    console.log(gui.scene.children[0].renderOrder = -1000);
    gui.loop();
};
