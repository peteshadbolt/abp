function poll() {
    console.log("polling");
    var xhr = new XMLHttpRequest();
    xhr.load=function() {
        console.log(JSON.parse(xhr.responseText));
    };

    xhr.onerror = function(e){
        console.log(e);
    };

    xhr.open("GET", "/state", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}

window.onload = function () {
    console.log("booting");
    setInterval(poll, 1000);
}
