define(["three", "orbitcontrols", "message"], function() {
    return {
        construct: function() {
            this.renderer = new THREE.WebGLRenderer();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setClearColor(0xffffff, 1);
            document.querySelector("body").appendChild(this.renderer.domElement);
            window.addEventListener("resize", this.onWindowResize, false);

            this.makeScene();

            this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.3, 1000);
            this.controls = new THREE.OrbitControls(this.camera);
            this.controls.center.set(0, 0, 0);
            this.controls.rotateSpeed = 0.2;
            this.camera.position.set(0, 0, 20);
            this.controls.addEventListener("change", this.render);
        },

        // Someone resized the window
        onWindowResize: function(evt) {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.render();
        },

        // Render the current frame to the screen
        render: function() {
            this.renderer.render(this.scene, this.camera);
        },

        // Make the extra bits of gui
        makeScene: function() {
            this.scene = new THREE.Scene();
            var grid = new THREE.GridHelper(10, 1);
            grid.rotation.x = Math.PI / 2;
            grid.setColors(0xdddddd, 0xeeeeee);
            this.scene.add(grid);
        }


    };
});
