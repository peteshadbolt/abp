console.log("abp v0.4.26");

window.onload = function() {
    graph.prepare();
    materials.prepare();
    gui.prepare();
    mouse.prepare();
    editor.prepare();
    gui.loop();
};
