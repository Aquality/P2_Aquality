var x = 0;

function birne() {
    fill(0,0,0);
    ellipse(x, 50, 50);
}

function draw(){
    clear();
    if(x<=400){
        x=x+5;
    }
    if(x==400){

    }
    birne();
    
}