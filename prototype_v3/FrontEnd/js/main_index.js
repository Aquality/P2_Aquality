var switched = false;

function draw() {
    getActualProduct();
    if(actualProduct != "nothing" && switched == false) {
        window.location = "scanscreen.html";
        switched = true;
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