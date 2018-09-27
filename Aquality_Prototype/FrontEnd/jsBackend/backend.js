var uri = "ws://localhost:8765";

//== WebSocket Initialisierung ==

var socket = new WebSocket(uri);

socket.onopen = function (event) {
    console.log("WebSocket opened");
}
socket.onclose = function (event) {
    console.log("WebSocket closed")
    socket = null;
}
socket.onmessage = function (event) {
    webSocketReceiveHandler(event);
}

//== FRONTEND VARIABLES ===
var products = [];
var totalWater = 0;
var actualProduct = "nothing";
var locked = false;

//=== FRONTEND FUNKTIONEN ===

function unlockScann() {
    socket.send("unlockScann");
}

function getActualProduct() {
    socket.send("getActualProduct");
}

function resetBackendActualProduct() {
    socket.send("resetBackendActualProduct");
}

function getTotalWater() {
    socket.send("getTotalWater");
}

function getProducts() {
    socket.send("getProducts");
}

function addProduct(productname, count) {
    socket.send("add " + productname + " " + count);
}

function deleteProduct(productname, count) {
    socket.send("delete " + productname + " " + count);
}

function printBill() {
    socket.send("printBill");
}

function resetBackend() {
    socket.send("resetBackend");
}

//=== WebSocket Funktionen ===

function webSocketReceiveHandler(event) {
    try {
        var jsonProducts = [];

        if(typeof JSON.parse(event.data) == "object") {
            jsonProducts = JSON.parse(event.data);
            for(var i = 0; i < jsonProducts.length; i++) {
                products[i] = JSON.parse(jsonProducts[i]);
            }
        }

    }

    catch(err) {

    }

    try {
        if(typeof JSON.parse(event.data) == 'number') {
        totalWater = JSON.parse(event.data);
        }
    }

    catch(err) {

    }

    try {
        if(typeof JSON.parse(event.data) == "string") {
            if(JSON.parse(event.data) == "locked") {
                locked = true;
            } else if(JSON.parse(event.data) == "unlocked") {
                locked = false;
            } else {
                actualProduct = JSON.parse(event.data);
            }

        }
    }

    catch(err) {

    }
    
}

//------------------------------------------------------------------------------------

/* function setup() {
    createCanvas(500, 500);
    frameRate(2);
}

function draw() {
if(socket.readyState === socket.OPEN) {
    getProducts();
}
} */

