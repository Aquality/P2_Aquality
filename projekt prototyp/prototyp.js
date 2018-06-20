

function onLoadedHandler() {

    var wasser = 0;

    var tomate = 40;
    var banane = 940;
    var avocado = 2000;
    var apfel = 700;
    var erdbeere =  276;
    var huhn = 3.900;
    
        
    
    document.getElementById('tomate').addEventListener('click',function(){
       wasser=wasser+tomate;
    });
    document.getElementById('banane').addEventListener('click',function(){
        wasser=wasser+banane; 
    });
    document.getElementById('avocado').addEventListener('click',function(){
        wasser=wasser+avocado;
    });
    document.getElementById('apfel').addEventListener('click',function(){
        wasser=wasser+apfel;
    });
    document.getElementById('erdbeere').addEventListener('click',function(){
        wasser=wasser+erdbeere;
    });
    document.getElementById('huhn').addEventListener('click',function(){
        wasser=wasser+huhn;
    });

    document.getElementById('berechnen').addEventListener('click',function(){
        alert('Ergebnis: '+wasser);
    }); 
    
    document.getElementById('reset').addEventListener('click',function(){
        wasser = 0;
    });

}



window.addEventListener('DOMContentLoaded' ,onLoadedHandler);