var switched = false;
function setup() {
    frameRate(2);
    createCanvas(1, 1);
}

function draw() {
    if(socket.readyState === socket.OPEN) {
    console.log("test");
    getActualProduct();
    if(actualProduct != "nothing" && switched == false) {
	console.log("test");
        window.location = "scanscreen.html";
        switched = true;
    }
    }
}


function keyPressed() {
    //scannt Tomate Ein
    if (keyCode == 84) {
        scanProduct();
    } else if (keyCode == 82) {
        console.log(products);
    }
}