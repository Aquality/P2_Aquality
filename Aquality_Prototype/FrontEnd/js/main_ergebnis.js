

var x = 0;

var counter = 0;

totalWater = 100;

function setup() {
    frameRate(15);
    document.getElementById('video').addEventListener('ended',myHandler,false);
    
}

function draw() {
    getTotalWater();
    days = totalWater / 1.5;
    document.getElementById("waterCount").innerHTML = Math.round(counter);

    if(counter < days) {
        counter += days / 50;
    } else {
        counter = days;
        if(x < 60) {
            x++;
        } else {
                document.getElementById("satz").style.opacity = 1;
        }
    }
}

function myHandler(e) {
    window.location = "ende.html";
}