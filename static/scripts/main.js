// Import modules
requirejs(["anders_briegel", "gui"], init);
var ab;

// Called on startup
function init(anders_briegel, gui) {
    ab = anders_briegel;
    gui.construct();
    gui.render();
}
