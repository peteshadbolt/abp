var url = "ws://localhost:8000/";

function doConnect() {
    websocket = new WebSocket(url);
    websocket.onopen = onOpen;
    websocket.onclose = onClose;
    websocket.onmessage = onMessage;
    websocket.onerror = onError;
}

function onOpen(evt) {
    writeToScreen("connected\n");
    doSend("Hello from the browser");
}

function onClose(evt) {
    writeToScreen("disconnected\n");
}

function onMessage(evt) {
    writeToScreen("response: " + evt.data + '\n');
}

function onError(evt) {
    writeToScreen('error: ' + evt.data + '\n');
    websocket.close();
}

function doSend(message) {
    writeToScreen("sent: " + message + '\n');
    websocket.send(message);
}

function writeToScreen(message) {
    console.log(message);
}

function init() {
    doConnect();
}

function doDisconnect() {
    websocket.close();
}

window.addEventListener("load", init, false);
