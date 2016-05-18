// Import modules
requirejs(["anders_briegel", "gui", "graph"], init);
var ab;

// Called on startup
function init(anders_briegel, gui, graph) {
    ab = anders_briegel;
    graph.hookEvents();
    gui.construct();
    gui.render();
}
