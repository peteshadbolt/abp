function bootstrap() {

    abj.add_node(0, {
        position: new THREE.Vector3(0, 0, 0)
    });
    abj.add_node(1, {
        position: new THREE.Vector3(1, 0, 0)
    });
    graph.update();
}

window.onload = function() {
    graph.prepare();
    materials.prepare();
    gui.prepare();
    mouse.prepare();
    editor.prepare();
    bootstrap();
    gui.loop();
};
