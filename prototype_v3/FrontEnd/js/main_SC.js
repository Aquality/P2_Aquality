function setup(){
    frameRate(2);
}

function addButton(produkt) {
    getProducts();
    addProduct(produkt, 1);
    for(var i = 0; i < products.length; i++) {

        if(products[i].name == produkt) {
            document.getElementById("counter"+produkt).innerHTML = products[i].count;
        }
    }
}

function deleteButton(produkt) {
    getProducts();
    for(var i = 0; i < products.length; i++) {

        if(products[i].count > 0) {
            deleteProduct(produkt, 1);
            if(products[i].name == produkt) {
                document.getElementById("counter"+produkt).innerHTML = products[i].count;
            }
        }
    }
}

function draw() {
    getProducts();
    console.log("test");
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