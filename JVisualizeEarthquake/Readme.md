# Unit 17 | Assignment - Visualizing Data with Leaflet

## Background

![1-Logo](Images/1-Logo.png)

The work is about helping United States Geological Survey, or USGS for short in building a new set of tools that will allow them visualize their earthquake data. 

## Tasks Done: 

### Step 1: Basic Visualization

![2-BasicMap](Images/2-BasicMap.png)

Visualize an earthquake data set.

1. **Get your data set**

   ![3-Data](Images/3-Data.png)

   The USGS provides earthquake data in a number of different formats, updated every 5 minutes. Visit the [USGS GeoJSON Feed](http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) page and pick a data set to visualize. When you click on a data set, for example 'All Earthquakes from the Past 7 Days', you will be given a JSON representation of that data. You will be using the URL of this JSON to pull in the data for our visualization.

   ![4-JSON](Images/4-JSON.png)

2. **Import & Visualize the Data**

   Create a map using Leaflet that plots all of the earthquakes from your data set based on their longitude and latitude.

   * Your data markers should reflect the magnitude of the earthquake in their size and color. Earthquakes with higher magnitudes should appear larger and darker in color.

   * Include popups that provide additional information about the earthquake when a marker is clicked.

   * Create a legend that will provide context for your map data.

   * Your visualization should look something like the map above.

- - -

### Step 2: More Data was overlayed with option to view tectonic plates

![5-Advanced](Images/5-1-VisualizeEarthQuake_IndexPageScreenShot.png)

Illustrates the relationship between tectonic plates and seismic activity. Data on tectonic plates was found at <https://github.com/fraxen/tectonicplates>.

In this step we are going to..

* Plot a second data set on our map.

* Add a number of base maps to choose from as well as separate out our two different data sets into overlays that can be turned on and off independently.

* Add layer controls to our map.

- - -

### Step 3: Time Keeps on Ticking

![7-NotGif](Images/6-Time_Keeps_On_Ticking.gif)

Many people don't know how much seismic activity is happening around them all the time. Did you know that Southern California has over 10,000 earthquakes each year alone? The USGS wants you to create a map that will visualize just how many earthquakes happen over the course of a day/week.

* A Leaflet plugin was used (they can be found at <http://leafletjs.com/plugins.html>) to visualize your earthquake as it takes place over a period of time.
