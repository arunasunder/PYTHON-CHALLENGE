//$.getScript('addressData.js', function() {
    //script is loaded and executed put your dependent JS here

//var imported = document.createElement('script');
//imported.src = 'addressData.js';
//document.head.appendChild(imported);

	var $tbody = document.querySelector("tbody");
	var $searchBtn = document.querySelector("#search");

	console.log(addressData);

	for (var i =0; i < addressData.length ; i++) {
		console.log("Element no. " + i);
		//for (var j =0 ; j < 6 ; j++) {

			console.log(addressData[i].id);
		//}

	}
	/* addressData.forEach( function (arrayItem)
	{
    	var x = arrayItem.id;
    	console.log(x + " " + arrayItem.Country); 
	}); */


	for (var i = 0; i < addressData.length; i++) {
		var $row = $tbody.insertRow(i);
		var addr1 = addressData[i];
		var fields = Object.keys(addr1)
		for (var j = 0; j < fields.length; j++) {

			var $cell = $row.insertCell(j);
			if (j == 0) {
				$cell.innerText  = addressData[i].id; //or field = fields[j] then access addr1[field];
			} else if (j == 1) {
				$cell.innerText  = addressData[i].country;
			} else if (j == 2) {
				$cell.innerText  = addressData[i].state;
			} else if (j == 3) {
				$cell.innerText  = addressData[i].city;
			} else if (j == 4) {
				$cell.innerText  = addressData[i].street_name;
			} else if (j == 5) {
				$cell.innerText  = addressData[i].street_number;
			} 

			//$cell.innerText = "Row " + (i + 1) + ", Cell " + (j  + 1);
		}

	}

	for (var i = 0; i < filteredaddress)

//});

$searchBtn = 