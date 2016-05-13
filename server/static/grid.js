//TODO Move to THREE.gridhelper
// Make a grid
function makeGrid(side, n, color) {
    var grid = new THREE.GridHelper(20, 2);
    grid.rotation.x = Math.PI/2;
    grid.setColors(0xdddddd, 0xeeeeee);
    return grid;
}
