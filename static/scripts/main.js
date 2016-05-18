function bootstrap(){
    graph.add_node(0, 0, 0);
    graph.add_node(3, 0, 0);
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
