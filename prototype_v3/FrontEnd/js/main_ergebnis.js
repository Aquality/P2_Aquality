//counter
var x = 0;

var shiftCounter = 0;
var shift = 190;

var faceShiftCount = 0;
var faceShift = 380;

var faceShiftCount2 = 0;

var scShiftCounter = 0;
var scShift = 450;

//Bilder Initialisieren

var wasserhahn;

var scene;

var face;

var einkaufswagen;

//tropfen

var tropfen;
var size;
var growFactor;
var waterCounter;
var maxSize;
var growFactorWater;
var textOffset;

var days;


function setup() {
    createCanvas(window.innerWidth, window.innerHeight);
    frameRate(15);


    //images
    wasserhahn = loadImage("ergebnis-icons/png/bearbeitet/wasserhahn.png");
    tropfen = loadImage("ergebnis-icons/png/bearbeitet/tropfen.png");
    face = loadImage("ergebnis-icons/png/bearbeitet/face.png");
    einkaufswagen = loadImage("ergebnis-icons/png/bearbeitet/einkaufswagen.png");

    //variablen

    scene = "start";

    size = 0;

    maxSize = 350;

    waterCounter = 0;

    growFactorWater = 3;


    textOffset = 0;

    getTotalWater();
    totalWater = 2132;

    days = totalWater / 1.5;
}

function draw() {

    if(scene == "start") {

        clear();
        background(0, 142, 138);
        calcGrowFactor();

        imageMode(CENTER);
        image(tropfen, 950, 180, size, size*3);
        imageMode(CORNER);
        fill(255);
        image(wasserhahn, -630, -100);


        textSize(size);
        textAlign(CENTER);

        if(size < maxSize) {
            size += growFactorWater;
            
            textOffset += 2.5;
        }

        if(waterCounter < days) {
            waterCounter += growFactor;
        } else if(waterCounter > days) {
            waterCounter = days;
            scene = "delay";
        }
        text(Math.round(waterCounter), 950, 240 + textOffset);

    } else if(scene == "delay") {
        if(x < 10) {
            x++;
        } else {
            scene = "animation";
        }
    } else if(scene == "animation") {
        background(0, 142, 138);

        imageMode(CENTER);
        image(tropfen, 950, 180 - shiftCounter, maxSize, maxSize*3);
        imageMode(CORNER);
        fill(255);
        image(wasserhahn, -630, -100 - shiftCounter);


        textSize(maxSize);
        textAlign(CENTER);
        text(Math.round(waterCounter), 950, 240 + textOffset - shiftCounter);
        
        if(shiftCounter < shift) {
            shiftCounter += 20;
        } else {
            scene="delay2";
        }
    } else if(scene == "delay2") {
        if(x < 10) {
            x++;
        } else {
            scene = "face";
        }
    } else if(scene == "face") {
        clear();
        background(0, 142, 138);

        imageMode(CENTER);
        image(tropfen, 950, 180 - shiftCounter, maxSize, maxSize*3);
        imageMode(CORNER);
        fill(255);
        image(wasserhahn, -630, -100 - shiftCounter);


        textSize(maxSize);
        textAlign(CENTER);
        text(Math.round(waterCounter), 950, 240 + textOffset - shiftCounter);

        image(face, 850, window.innerHeight - faceShiftCount);

        if(faceShiftCount < faceShift) {
            faceShiftCount += 3;
        } else {
            scene = "einkaufswagen"
        }
    } else if(scene == "einkaufswagen") {
        clear();
        background(0, 142, 138);

        imageMode(CENTER);
        image(tropfen, 950, 180 - shiftCounter, maxSize, maxSize*3);
        imageMode(CORNER);
        fill(255);
        image(wasserhahn, -630, -100 - shiftCounter);


        textSize(maxSize);
        textAlign(CENTER);
        text(Math.round(waterCounter), 950, 240 + textOffset - shiftCounter);

        image(face, 850 + faceShiftCount2, window.innerHeight - faceShift);

        image(einkaufswagen, 0 + scShiftCounter, window.innerHeight - 400);

        if(scShiftCounter < scShift) {
            scShiftCounter += 170;
        } else {
            if(faceShiftCount2 < faceShift*2) {
                faceShiftCount2 += 170;
            }
        }
    }

}

function calcGrowFactor() {
    growFactor = (days / maxSize) * growFactorWater;
}



//===================================================================000
function keyPressed() {
    //scannt Tomate Ein
    if (keyCode == 84) {
        scanProduct();
    } else if (keyCode == 82) {
        console.log(products);
    }
}