var totalWater = 0;
var products = [];
var actualProduct;

//Platzhalter Variablen
var backendActualProduct = "nothing";
var water;
var backendProducts = [];


//=== FrontEnd Funktionen ===

function getActualProduct() {
    actualProduct = backendActualProduct;
}

function resetbackendActualProduct() {
    backendActualProduct = "nothing";
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
            backendProducts.push(new Product(productname, count, 150));
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
    console.log("BACKEND RESETTET");
}

//=== Funktionen, damit der Platzhalter Funktioniert ===

function scanProduct() {

    if(backendActualProduct != "Tomate") {
        backendActualProduct = "Tomate";
        console.log("TOMATE EINGESCANNT");
        for(var i = 0; i <= backendProducts.length; i++) {

            if(i == backendProducts.length) {
                backendProducts.push(new Product("Tomate", 4, 150));
                break;
            } else if(backendProducts[i].name == "Tomate") {
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
    constructor(name, count, water) {
        this.name = name;
        this.count = count;
        this.water = water;
    }
}