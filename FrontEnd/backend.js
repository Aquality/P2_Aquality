//=== Backend Variables ===

totalWater;
purchasedProducts = [];

//=== WebSocket Variables ===

socket = null;
uri = "ws://localhost:8765";


//=== WebSocket Funktionen ===

function sendToBackend(message) {
    socket = new WebSocket(uri);
    socket.onopen = function (e) { console.log("opened " + uri);
        webSocketSend(message);
    };
    socket.onclose = function (e) { console.log("closed"); socket = null;};
    socket.onmessage = function (e) { console.log("Server: " + e.data); };
    socket.onerror = function (e) { if (e.data) console.log("Error: " + e.data); };
}


function webSocketSend(message) {
    if (socket == null) {
        console.log("socket is not connected");
        return;
    }
    socket.send(message);
}

function webSocketDisconnect() {
    socket.close();
}


//=== FrontEnd Funktionen ===

function getBackendVariables() {
    if(socket.readyState === socket.CLOSED) {
        sendToBackend("getBackendVariables");
    }
}

function addProduct(productname) {
    sendToBackend("add " + productname);
}

function deleteProduct(productname) {
    sendToBackend("delete " + productname);
}

function printBill() {
    sendToBackend("print");
}

function checkScanner() {
    if()
}