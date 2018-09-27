function setup(){
    frameRate(2);
}

function addButton(produkt) {
    addProduct(produkt, 1);
    document.getElementById("counter"+produkt).innerHTML++;
}

function deleteButton(produkt) {
    for(var i = 0; i < products.length; i++) {
	if(products[i].name == produkt) {
            if(products[i].count > 0) {
                deleteProduct(produkt, 1);
		document.getElementById("counter"+produkt).innerHTML--;
            }
        }
    }
}

function draw() {
    getProducts();
    getTotalWater();
    for(var i = 0; i < products.length; i++) {

	if(document.getElementById("counter"+products[i].name) == null){

        document.getElementById("productTable").innerHTML =
	document.getElementById("productTable").innerHTML +
        "<table>"+
            "<tr>"+
                "<th class=\"minus\"></th>"+
                "<th class=\"counter\"></th>"+
                "<th class=\"product\"></th>"+
                "<th class=\"plus\"></th>"+
           "</tr>" +
            "<div id=\"scannedProducts\">"+
        "<tr>"+
                    "<td class=\"minus\">"+
                        "<button id=\"minus-button-SC\" onclick=\"deleteButton(\'" +  products[i].name + "\')\" type=\"button\" class=\"btn btn\">-</button>"+
                    "</td>"+
                    "<td class=\"counter\" id=\"counter"+ products[i].name +"\">" + products[i].count +"</td>" +
                    "<td class=\"product\" id=\"produktName\">" + products[i].name + "</td>" +
                    "<td class=\"plus\">" +
                        "<button id=\"plus-button-SC\" onclick=\"addButton(\'" + products[i].name + "\')\" type=\"button\" class=\"btn btn\">" +
                            "+" +
                        "</button>"+
                    "</td>"+
        "</tr>"+
        "</div>"+
        "</table>"

	}
	document.getElementById("counter"+products[i].name).innerHTML = products[i].count;
    }

    document.getElementById("bodyCount").innerHTML = 
        "... nimmst du einem Menschen <span style=\"color: rgb(255, 61, 59); font-size:2em;\">"+
        Math.round(totalWater / 1.5 ) +
        "</span> Tage das Trinkwasser weg.";

    if(totalWater < 100) {
        console.log("test");
        document.getElementById("dorfImg").src = "dorf-screens/svg/Stufe 1.svg";
        document.getElementById("industrieImg").src = "industrie-screens/svg/Stufe 5.svg";
    }
    else if(totalWater < 500) {
        console.log("test");
        document.getElementById("dorfImg").src = "dorf-screens/svg/Stufe 2.svg";
        document.getElementById("industrieImg").src = "industrie-screens/svg/Stufe 4.svg";
    }
    else if(totalWater < 2000) {
        console.log("test");
        document.getElementById("dorfImg").src = "dorf-screens/svg/Stufe 3.svg";
        document.getElementById("industrieImg").src = "industrie-screens/svg/Stufe 3.svg";
    }
    else if(totalWater < 10000) {
        console.log("test");
        document.getElementById("dorfImg").src = "dorf-screens/svg/Stufe 4.svg";
        document.getElementById("industrieImg").src = "industrie-screens/svg/Stufe 2.svg";
    }
    else if(totalWater < 20000) {
        console.log("test");
        document.getElementById("dorfImg").src = "dorf-screens/svg/Stufe 5.svg";
        document.getElementById("industrieImg").src = "industrie-screens/svg/Stufe 1.svg";
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