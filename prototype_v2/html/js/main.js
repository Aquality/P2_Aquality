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

//=== FRONTEND FUNKTIONEN ===

function getVariables() {

    socket.send("getVariables");

}

function getTotalWater() {

    socket.send("getTotalWater");

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
        } else {

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
    
}

//------------------------------------------------------------------------------------

function setup() {
    createCanvas(500, 500);
    frameRate(30);
}

function draw() {
if(socket.readyState === socket.OPEN) {
    getVariables();
    getTotalWater();
    console.log(products);
    console.log(totalWater);
}
}

