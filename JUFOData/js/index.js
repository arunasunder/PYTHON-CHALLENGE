// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $stateInput = document.querySelector("#state");
var $searchBtn = document.querySelector("#search");

var $datetimeInput = document.querySelector("#datetime");
var $cityInput = document.querySelector("#city");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");

var $pagination = $('#pagination'),
    totalRecords = 0,
    records = [],
    displayRecords = [],
    recPerPage = 25,
    page = 1,
    totalPages = 0;

//var $pagination_final = $('#pagination');

var defaultOpts = {
        totalPages: 20
};

//$pagination.twbsPagination(defaultOpts);

//Load headings with blue color.
document.getElementById("tableHeading").style.color = "darkblue";

// Add an event listener to the searchButton, call handleSearchButtonClick when clicked
$searchBtn.addEventListener("click", handleSearchButtonClick);

//var startingIndex = 0;
//var resultsPerPage = 50;

// Set filteredData to dataSet initially
//var filteredData = dataSet;
records = dataSet;


function toProperCase(s)
{
  return s.toLowerCase().replace(/^(.)|\s(.)/g, 
          function($1) { return $1.toUpperCase(); });
}

function generate_table() {
    //var tr;
    $tbody.innerHTML = "";
    for (var i = 0; i < displayRecords.length; i++) {
        // Get get the current UFO Data object and its fields
        var UFOData = displayRecords[i];
        var fields = Object.keys(UFOData);
        // Create a new row in the tbody, set the index to be i + startingIndex
        var $row = $tbody.insertRow(i);
        for (var j = 0; j < fields.length; j++) {
          // For every field in the UFOData object, create a new cell at set its inner text to be the current value at the current UFOData's field
          var field = fields[j];
          var $cell = $row.insertCell(j);
          if (j == 2 || j == 3) {
            $cell.innerText = (UFOData[field]).toUpperCase();
          } else if (j == 1 || j == 4) {
              $cell.innerText = toProperCase(UFOData[field]);
          } else {
              $cell.innerText = UFOData[field];
          }
        }
      }
}

function handleSearchButtonClick() {

  console.log("Entered fucntion for SerachButton Click");

  // Format the user's search by removing leading and trailing whitespace, lowercase the string
    var filterDateTime = $datetimeInput.value.trim().toLowerCase();
    var filterCity = $cityInput.value.trim().toLowerCase();
    var filterState = $stateInput.value.trim().toLowerCase();
    var filterCountry = $countryInput.value.trim().toLowerCase();
    var filterShape = $shapeInput.value.trim().toLowerCase();

    // Set filteredData to an array of all UFO Data who's data matches all the filters 
    records = dataSet.filter(function(UFO_data) {
        var searchDateTime = UFO_data.datetime.substring(0, filterDateTime.length).toLowerCase();
        var searchCity = UFO_data.city.substring(0, filterCity.length).toLowerCase();
        var searchState = UFO_data.state.substring(0, filterState.length).toLowerCase();
        var searchCountry = UFO_data.country.substring(0, filterCountry.length).toLowerCase();
        var searchShape = UFO_data.shape.substring(0, filterShape.length).toLowerCase();

        if (searchDateTime === filterDateTime && searchCity === filterCity && searchState === filterState && searchCountry === filterCountry && searchShape === filterShape) {
            return true;
        }
        return false;
    });

    console.log("----Filtered Records START----")
    console.log(records);
    console.log("----Filtered Records END----")

    totalRecords = records.length;
    totalPages = Math.ceil(totalRecords / recPerPage);

    //Destroy pagination and recreate the pagination of records 
        
    $pagination.twbsPagination('destroy');
    $pagination.twbsPagination($.extend({}, defaultOpts, {
        startPage: 1,
        totalPages: totalPages,
        visiblePages: 6,
        onPageClick: function (event, page) {
          displayRecordsIndex = Math.max(page - 1, 0) * recPerPage;
          endRec = (displayRecordsIndex) + recPerPage;
          console.log(displayRecordsIndex + 'ssssssssss'+ endRec);
          displayRecords = records.slice(displayRecordsIndex, endRec);
          generate_table();
        }
    }));
}

function apply_pagination() {

    console.log("Entered apply pagination function");
    $pagination.twbsPagination({
      totalPages: totalPages,
      visiblePages: 6,
      onPageClick: function (event, page) {
        displayRecordsIndex = Math.max(page - 1, 0) * recPerPage;
        endRec = (displayRecordsIndex) + recPerPage;
        console.log(displayRecordsIndex + 'ssssssssss'+ endRec);
        displayRecords = records.slice(displayRecordsIndex, endRec);
        generate_table();
      }
    });
  }
/*
function handleSearchButtonClick() {
  // Format the user's search by removing leading and trailing whitespace, lowercase the string
  var filterState = $stateInput.value.trim().toLowerCase();

  if (filterState == "all") { 
    filteredData = dataSet;   
  } else {
    // Set filteredData to an array of all UFOData whose "state" matches the filter
    filteredData = dataSet.filter(function(UFO_data) {
      var State = UFO_data.state.toLowerCase();

      // If true, add the UFOData to the filteredData, otherwise don't add it to filteredData
      return State === filterState;
    });

  }
  
  renderTable();
} */


// Render the table for the first time on page load
//renderTable();

console.log(records);
totalRecords = records.length;
totalPages = Math.ceil(totalRecords / recPerPage);
apply_pagination();
