var body;
var state;

function poll() {
    var xhr = new XMLHttpRequest();

    xhr.onload = function() {
        state = JSON.parse(xhr.responseText);
        console.log(state);
        //soft_console.innerHTML = "\n" + xhr.responseText;
    };

    xhr.onerror = function(e){
        //soft_console.innerHTML = "\n" + "Lost connection to server";
    };

    xhr.open("GET", "/state", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}
