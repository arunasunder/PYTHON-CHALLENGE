# Belly Button Biodiversity

![Bacteria by filterforge.com](static/bacteria_by_filterforgedotcom.jpg)



## Step 1 - Flask API

Flask was used to design an API for the dataset and to serve the HTML and JavaScript required for your dashboard page. sqlite database was used. 

* First, create a template called `index.html` for your dashboard landing page. Use the Bootstrap grid system to create the structure of the dashboard page.

* The following routes have been created and these endpoints were used to plot the plotly charts. 

```python
@app.route("/")
    """Return the dashboard homepage."""
```
```python
@app.route('/names')
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]

    """
```
```python
@app.route('/otu')
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
```
```python
@app.route('/metadata/<sample>')
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
```
```python
@app.route('/wfreq/<sample>')
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """
```
```python
@app.route('/samples/<sample>')
    """OTU IDs and Sample Values for a given sample.

    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]
    """
```

---

## Step 2 - Plotly.js

Plotly.js was used to build interactive charts for my dashboard. The endpoitns created were called and used to pull data out to be used for Plotly D3 bubble and pie plots as well as for the gauge. 

* Used the route `/names` to populate a dropdown select element with the list of sample names.

  * Use `document.getElementById`, `document.createElement` and `append` to populate the create option elements and append them to the dropdown selector.

  * Use the following HTML tag for the dropdown selector

  ```html
  <select id="selDataset" onchange="optionChanged(this.value)"></select>
  ```
  * Create a function called `optionChanged` to handle the change event when a new sample is selected (i.e. fetch data for the newly selected sample).

  ![dropdown](Images/dropdown.png)

* Created a PIE chart that uses data from your routes `/samples/<sample>` and `/otu` to display the top 10 samples.

  * Used the Sample Value as the values for the PIE chart

  * Used the OTU ID as the labels for the pie chart

  * Used the OTU Description as the hovertext for the chart

  * Used `Plotly.restyle` to update the chart whenever a new sample is selected


* Created a Bubble Chart that uses data from your routes `/samples/<sample>` and `/otu` to plot the __Sample Value__ vs the __OTU ID__ for the selected sample.

  * Used the OTU IDs for the x values

  * Used the Sample Values for the y values

  * Used the Sample Values for the marker size

  * Used the OTU IDs for the marker colors

  * Used the OTU Description Data for the text values

  * Used `Plotly.restyle` to update the chart whenever a new sample is selected

* Display the sample metadata from the route `/metadata/<sample>`

  * Display each key/value pair from the metadata JSON object somewhere on the page

  * Update the metadata for each sample that is selected

* Did some updates to the dashboard index page to have some character. Also, made the container fluid to realign the charts wehn size of window is shrunk. 

* Finally, deployed Flask app to Heroku.

---

## Optional Challenge Part

* A gauge Chart was adapted from [https://plot.ly/javascript/gauge-charts/](https://plot.ly/javascript/gauge-charts/) to plot the Weekly Washing Frequency obtained from the route `/wfreq/<sample>`

* Gauge code was updated to account for values ranging from 0 - 9.

* Used `Plotly.restyle` to update the chart whenever a new sample is selected


