function poll() {
    var xhr = new XMLHttpRequest();

    xhr.onload=function() {
        console.log(xhr.responseText);
    };

    xhr.onerror = function(e){
    };

    xhr.open("GET", "/state", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}

window.onload = function () {
    console.log("booting");
    setInterval(poll, 1000);
}
