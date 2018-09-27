var totalWater = 0;
var products = [];
var actualProduct;

//Platzhalter Variablen
var backendActualProduct = "nothing";
var water;
var backendProducts = [];
var locked = false;

//=== FrontEnd Funktionen ===


function unlockScann() {
    console.log("Scanning is now unlocked");
    locked = false;
}

function getActualProduct() {
    actualProduct = backendActualProduct;
}

function resetBackendActualProduct() {
    backendActualProduct = "nothing";
    locked = false;
}

function getTotalWater() {
    totalWater = calculateWater();
}

function getProducts() {
    products = [];
    for(var i = 0; i < backendProducts.length; i++) {
        products[i] = backendProducts[i];
    }
}

function addProduct(productname, count) {
    for(var i = 0; i <= backendProducts.length; i++) {
        
        if (i == backendProducts.length){
            backendProducts.push(new Product(productname, count, 150, 4));
            break;
        } else if(productname == backendProducts[i].name) {
            backendProducts[i].count += count;
            break;
        }

    }
}

function deleteProduct(productname, count) {
    for(var i = 0; i <= backendProducts.length; i++) {

        if(productname == backendProducts[i].name) {
            backendProducts[i].count -= count;
            if(backendProducts[i].count <= 0) {
                backendProducts.splice(i, 1);
            } 
            return;
        }

    console.log("Mehr Produkte entfernt, als im Einkaufswagen vorhanden!");

    }
}

function printBill() {
    console.log("DRUCKE RECHNUNG");
}

function resetBackend() {
    backendProducts = null;
    backendProducts = [];
    locked = false;
    console.log("BACKEND RESETTET");
}

//=== Funktionen, damit der Platzhalter Funktioniert ===


function lockScann() {
    console.log("Scanning is now locked");
    locked = true;
}

function scanProduct() {

    if(backendActualProduct != "Mais" && locked == false) {
        lockScann();
        backendActualProduct = "Mais";
        console.log("Mais EINGESCANNT");
        for(var i = 0; i <= backendProducts.length; i++) {

            if(i == backendProducts.length) {
                backendProducts.push(new Product("Mais", 1, 150, 1));
                break;
            } else if(backendProducts[i].name == "Mais") {
                break;
            }
        }
    }
}

function calculateWater() {
    water = 0;
    for(i = 0; i < backendProducts.length; i++) {
        water = water + backendProducts[i].water * backendProducts[i].count;
    }
    return water;
}

class Product {
    constructor(name, count, water, startCount) {
        this.name = name;
        this.count = count;
        this.water = water;
        this.startCount = startCount;
    }
}