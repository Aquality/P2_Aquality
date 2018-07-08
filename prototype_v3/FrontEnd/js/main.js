/*
================================================================================================
== KOMMUNIKATION MIT DEM BACKEND ==
================================================================================================

Variablen:

var totalWater;
var products = [];
actualProduct;


Funktionen:

--------------------------------------------------------------
getActualProduct()

    aktualisiert die Variable >> actualProduct <<, welche angibt, welches Produkt als letztes vom user eingescannt wurde
    zB. "Tomate"
--------------------------------------------------------------


--------------------------------------------------------------
resetActualProduct()

    resettet die Variable, des zuletzt eingescannten Produktes (im Backend).
    Wird nun getActualProduct() aufgerufen, gibt die Funktion so lange
    den String "nothing" zurück, bis der Nutzer erneut ein Produkt einscannt.

--------------------------------------------------------------


--------------------------------------------------------------
getTotalWater()

    aktualisiert die Variable >> totalWater << auf den aktuellen Wert, welcher im Backend berechnet wird
    zB. totalWater = 1303;
--------------------------------------------------------------


---------------------------------------------------------------
getProducts()

    synchronisiert das Array >> products << mit den Werten im Backend.

    Im Array >> products << werden alle Produkte als Objekte gespeichert, welche momentan im Einkaufswagen des Nutzers
    gespeichert sind.

    Ein product-Objekt hat die attribute:
        name    -->     name des Produktes zB. "Tomate"
        count   -->     gibt an, wie viele Produkte des jeweiligen Typs im Einkaufswagen liegen
        water   -->     gibt an wie viel Wasser im jeweiligen Produkt enthalten ist
        startCount --> gibt an, mit wie vieln einheiten gestartet werden soll
---------------------------------------------------------------


---------------------------------------------------------------
addProduct(productname, count)

    fügt ein Produkt-Objekt mit dem jeweiligen Faktor >> count <<, dem Einkaufswagen hinzu.

    zB. addProduct("Tomate", 4);
        --> Fügt dem Einkaufswagen 4 Tomaten hinzu

    !ACHTUNG!
        Die Funktion getProducts(), muss zusätzlich aufgerufen werden, um die hinzugefügten Objekte
        im Frontend zu aktualisieren
    !Achtung!

---------------------------------------------------------------


---------------------------------------------------------------
deleteProduct(productname, count)

    Reduziert den >> count << Faktor eines product-Objektes um die angegebene Zahl (im Backend).
    Falls sich der >> count << Faktor eines product-Objektes auf 1 befindet, wird es aus dem Einkaufswagen (im Backend) gelöscht.

    zB. deleteProduct("Tomate", 2);
        --> löscht 2 Tomaten aus dem Einkaufswagen

    !ACHTUNG!
        Die Funktion getProducts(), muss zusätzlich aufgerufen werden, um die gelöschten Objekte
        im Frontend zu aktualisieren
    !Achtung!

---------------------------------------------------------------

---------------------------------------------------------------
printBill()

    gibt dem Drucker den Befehl, die Rechnung zu generieren und aus zu drucken

---------------------------------------------------------------

---------------------------------------------------------------
resetBackend()

    resettet das Backend so, dass die Simulation von vorne Beginnen kann.
    
    Sollte am Ende ein mal aufgerufen werden könnens

---------------------------------------------------------------

===========================================================================================================================
===========================================================================================================================
*/

/*

Drücke >> t << um eine Tomate ein zu scannen

wird ein Produkt eingescannt wird es automatisch als Product-Objekt dem products Array (im Backend) hinzugefügt.
Dabei erhält es den jeweiligen Count, welcher in der Datenbak als startCount definiert ist.

    zB. Scannt man eine Tomate ein, wird ein product Objekt dem Backend hinzugefügt mit den Attributen:
        name = "Tomate"
        count = 4 (da in unserem Paper Prototype 4 Tomaten in einer Schachtel sind)
        water = 150;

*/

//==========================================================================================================================
//==========================================================================================================================

//=== Variablen ===

var productCounter = 0;

function setup() {
    frameRate(2);
}

function draw() {
    getActualProduct();
    getProducts();
    imgChanger(actualProduct);
    document.getElementById("plus-button").style.display = "none";
    document.getElementById("minus-button").style.display = "none";
    document.getElementById("cancel").style.display = "none";
    document.getElementById("addToShoppingCart").style.display = "none";
    if (actualProduct != "nothing") {
        document.getElementById("productCounter").style.display = "inline-block";
        document.getElementById("plus-button").style.display = "inline-block";
        document.getElementById("minus-button").style.display = "inline-block";
        document.getElementById("cancel").style.display = "inline-block";
        document.getElementById("addToShoppingCart").style.display = "inline-block";
        for (var i = 0; i < products.length; i++) {
            if (products[i].name == actualProduct) {
                if (productCounter == 0) {
                    productCounter = products[i].startCount;
                    document.getElementById("productCounter").innerHTML = productCounter;
                }
            }
        }
    } else {
        document.getElementById("productCounter").style.display = "none";
    }
}

function imgChanger(product) {
    //aktualisiert die Produktanzeige
    document.getElementById("product").src = "icons/" + product + ".svg";
}

function addButton() {
    //Fügt der Produktmenge +1 des jeweiligen Produktes hinzu 
    productCounter++;
    document.getElementById("productCounter").innerHTML = productCounter;
    document.getElementById("plus").innerHTML = productCounter;

}

function deleteButton() {


    if (productCounter > 1) {
        productCounter--;
    }
    document.getElementById("productCounter").innerHTML = productCounter;
    document.getElementById("minus").innerHTML = productCounter;
}

function addSC() {
    //aktualisiert die Produktdaten nach Eingabe und Bestätigung der Menge
    addProduct(actualProduct, productCounter);


    for (var i = 0; i < products.length; i++) {
        if (products[i].name == actualProduct) {
            console.log(products[i].count);
        }
    }

    resetBackendActualProduct();
    unlockScann();
    productCounter = 0;
    document.getElementById("productCounter").innerHTML = productCounter;
}

function cancel() {
    resetBackendActualProduct();
    productCounter = 0;
    document.getElementById("productCounter").innerHTML = productCounter;
}


function keyPressed() {
    //scannt Tomate Ein
    if (keyCode == 84) {
        scanProduct();
    } else if (keyCode == 82) {
        console.log(products);
    }
}