# UFO Sightings Data - Javscript and DOM Manipulation 

## Background

Our UFO Sightings Data collection is too large to search through manually. Even our most dedicated followers are complaining that they are having trouble locating specific reports in this mess.

We need ability to: 
* Create table dynamically 
* Allow our users to search through the table for specific pieces of information. using pure JavaScript, HTML, and CSS on our web pages. 

## Solution

By: Aruna Amaresan (Ana Sunder) 
On: March 14th 2018

* I have used jQUERY bootstrap pagination v.1.4.1 to provide the pagiantion options for the json data - Referenced - Reference file is added 

* Search filters can be used in any combination 

* Parsed the data to show in Proper case for City Name and Shape. 

* Parsed data to ensure Country and State is in Upper Case  

## TasksCompleted

### Level 1: Automatic Table and Date Search

* Create a basic HTML web page.

* Using the ufo dataset provided in the form of a JavaScript object, write code that appends a table to your web page and then adds new rows of data for each UFO sighting.

  * Make sure you have a column for `date/time`, `city`, `state`, `country`, `shape`, and `comment` at the very least.

* Add an `input` tag to your HTML document and write JavaScript code that will search through the `date/time` column to find rows that match user input.

### Level 2: Multiple Search Categories

* Complete all of Level 1 criteria.

* Using multiple `input` tags and/or select dropdowns, write JavaScript code so the user can to set multiple filters and search for UFO sightings using the following criteria based on the table columns: 

  1. `date/time`
  2. `city`
  3. `state`
  4. `country`
  5. `shape`

### Level 3: Paginated Table

* Complete all of Level 2 criteria.

* Write code that will paginate the table (client-side pagination) and only display a maximum set number of results at a time (e.g. 50 results per page). Use [Bootstrap's Pagination Components](http://getbootstrap.com/components/#pagination) and write code to handle page changes and calculate the number of results which should appear on each page. 
* These changes should happen in the DOM using JavaScript, therefore the user should never be directed to another web page as they paginate through the results.

- - -

### Dataset

* [UFO Sightings Data](Data/data.js)


