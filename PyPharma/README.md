

```python
# Pymaceuticals Pharma Drug Analysis 
# Done by: Aruna Amaresan 
# Completion Date: Dec 18th 2017 
# Assumptions: 
# Pymaceuticals - Clinical Drug Analysis - 
# We are looking at the mean (average) of values when summarizing Tumer Volume Chnage over 'n' mice say using Drug 'C' 
# At each Time period of T=0. Then T = 5, 10 and so on. The same is done Metastatis Spread. We espect nit many outliers 
# present in the data set shared. hence taken mean. 
# For Survival Rate, we have taken the mouse count for each drug in ech time period. 
# 
# Input:   The two raw CSV files are expcetdd to be kept at the raw_data folder under this current directory. 
#          Their names are hard coded here. We can change it to be input of needed 
# Process: Data has been read from CS and first some clean-up and preparation of data done to be able to come up with 
#          results needed for the plots. 
# Output:  The following plots have been created. 
#          a) Tumor Volume Change over Time for all 4 drugs (compared) - Scatter Plot
#          b) Metastatis Spread of the cancer over time during the Drug treatment  - Scatter Plot 
#          c) Survival Rate over time By Drug - Scatter Plot 
#          d) % Tumor Volume Change By Drug - Bar Plot 
#          e) PDF file sharing an analysis of the three observable trends and next steps have been submitted 
#             also in this folder. Also shared a marked down Readme.MD file           

# Dependencies
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
import seaborn as sns
```


```python
# Load the  CSV file 
# Read CSV
#clinical_pd = pd.read_csv("raw_data\clinicaltrail_data.csv")
#mouse_drug_pd = pd.read_csv("raw_data\mouse_drug_data.csv")


# load the clinical CSV files 
clinicalCSV = os.path.join('raw_data', 'clinicaltrial_data.csv')

clinical_pd = pd.read_csv(clinicalCSV, encoding="iso-8859-1", low_memory=False)

clinical_pd.head()


#cleanse of any empty rows in students

clinical = clinical_pd.dropna(how="any")
clinical.head()


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mouse ID</th>
      <th>Timepoint</th>
      <th>Tumor Volume (mm3)</th>
      <th>Metastatic Sites</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>b128</td>
      <td>0</td>
      <td>45.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>f932</td>
      <td>0</td>
      <td>45.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>g107</td>
      <td>0</td>
      <td>45.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>a457</td>
      <td>0</td>
      <td>45.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>c819</td>
      <td>0</td>
      <td>45.0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Load the mouse ID to drug mapping CSV file 
mouse_drugCSV = os.path.join('raw_data', 'mouse_drug_data.csv')

mouse_drug_pd = pd.read_csv(mouse_drugCSV, encoding="iso-8859-1", low_memory=False)

#mouse_drug_pd.head()

#Cleanse any empty rows. 

mouse_drug = mouse_drug_pd.dropna(how="any")
mouse_drug.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mouse ID</th>
      <th>Drug</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>f234</td>
      <td>Stelasyn</td>
    </tr>
    <tr>
      <th>1</th>
      <td>x402</td>
      <td>Stelasyn</td>
    </tr>
    <tr>
      <th>2</th>
      <td>a492</td>
      <td>Stelasyn</td>
    </tr>
    <tr>
      <th>3</th>
      <td>w540</td>
      <td>Stelasyn</td>
    </tr>
    <tr>
      <th>4</th>
      <td>v764</td>
      <td>Stelasyn</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Merge the 2 data using MouseID   
clinical_mouse_drug_data = pd.merge(clinical, mouse_drug, on="Mouse ID")

count = len(clinical_mouse_drug_data)

#print("No. of Inner join records: %s" %(str(count)))

#clinical_mouse_drug_data.head(1000)
```


```python
# Take only columns we need from mouse_drug for lot on Tumer volume over Time plot 
#Mouse ID	Timepoint	Tumor Volume (mm3)
reduced_mouse_drug = clinical_mouse_drug_data.loc[:, ['Drug','Timepoint','Tumor Volume (mm3)']]

reduced_mouse_drug.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Drug</th>
      <th>Timepoint</th>
      <th>Tumor Volume (mm3)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Capomulin</td>
      <td>0</td>
      <td>45.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Capomulin</td>
      <td>5</td>
      <td>45.651331</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Capomulin</td>
      <td>10</td>
      <td>43.270852</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Capomulin</td>
      <td>15</td>
      <td>43.784893</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Capomulin</td>
      <td>20</td>
      <td>42.731552</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Group By Schools and Find Average reading score

clincial_ByDrug = pd.DataFrame(reduced_mouse_drug.groupby(['Drug','Timepoint'])['Tumor Volume (mm3)'].mean())

#clincial_ByDrug.head(100)

clincial_ByDrug_Updated = clincial_ByDrug.reset_index()

clincial_ByDrug.head(100)
#clincial_ForCapomulin.head()

y_max_value = clincial_ByDrug["Tumor Volume (mm3)"].max()

y_min_value = clincial_ByDrug["Tumor Volume (mm3)"].min()

#print ("Max: %s Min: %s" % (y_max_value, y_min_value))
```


```python
# Group By Drugs and Append to the cleaned up list
clinical_ForCapmoulin = reduced_mouse_drug[reduced_mouse_drug['Drug'] == "Capomulin"].groupby('Timepoint')['Tumor Volume (mm3)'].mean()


Capmoulin_pd = pd.DataFrame (clinical_ForCapmoulin)

Capmoulin_pd.reset_index(inplace = True)

Capmoulin_pd.rename(columns={"Tumor Volume (mm3)":"Capomulin"}, inplace = True)

# Data set needed for Part 4 bar plot  for Drug 1 - Caclulate & store while traversing the Tumor Volume Data 
# Create a holder for storing Tumor Volume Change over time for each drug - This would be used later to show 
# % Tumor size change over time

columnsHeaders = ['Drug Name', 'Original Volume', 'Volume Change', '% Tumor Volume Change']
Tumor_Percent_Change_ByDrug = pd.DataFrame(columns = columnsHeaders)

# Calculate the Original Size, Volume Change 
OriginalVolSize = 0
VolumeChange = 0

for index, row in Capmoulin_pd.iterrows():
    if (row["Timepoint"] == 0):
        OriginalVolSize = row["Capomulin"]
    
    if (row["Timepoint"] == 45):
        VolumeChange = row["Capomulin"] - OriginalVolSize
        break;

#print ("Original Vol Size: %s Volume Change: %s" %(str(OriginalVolSize), str(VolumeChange)))

#Add the values found into the appropriate columns - Then calculate & store % Volume Change 
index = 0
Tumor_Percent_Change_ByDrug.set_value(index, "Drug Name", "Capomulin")
Tumor_Percent_Change_ByDrug.set_value(index + 1, "Drug Name", "Infubinol")
Tumor_Percent_Change_ByDrug.set_value(index + 2, "Drug Name", "Ketapril")
Tumor_Percent_Change_ByDrug.set_value(index + 3, "Drug Name", "Placebo")

Tumor_Percent_Change_ByDrug.set_value(index, "Original Volume", OriginalVolSize)
Tumor_Percent_Change_ByDrug.set_value(index, "Volume Change", VolumeChange)
Tumor_Percent_Change_ByDrug.set_value(index, "% Tumor Volume Change", (VolumeChange / OriginalVolSize) * 100)

#print (Tumor_Percent_Change_ByDrug.head())

#Infubinol_pd["Infubinol Survival Rate %"] = Infubinol_pd["Infubinol"] / Total_MouseCount * 100

Capmoulin_pd.head(20)


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Timepoint</th>
      <th>Capomulin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>45.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
      <td>44.266086</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10</td>
      <td>43.084291</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>42.064317</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>40.716325</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
      <td>39.939528</td>
    </tr>
    <tr>
      <th>6</th>
      <td>30</td>
      <td>38.769339</td>
    </tr>
    <tr>
      <th>7</th>
      <td>35</td>
      <td>37.816839</td>
    </tr>
    <tr>
      <th>8</th>
      <td>40</td>
      <td>36.958001</td>
    </tr>
    <tr>
      <th>9</th>
      <td>45</td>
      <td>36.236114</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Group By Drugs and Append to the cleaned up list
clinical_ForInfubinol = reduced_mouse_drug[reduced_mouse_drug['Drug'] == "Infubinol"].groupby('Timepoint')['Tumor Volume (mm3)'].mean()


Infubinol_pd = pd.DataFrame (clinical_ForInfubinol)

Infubinol_pd.reset_index(inplace = True)
Infubinol_pd.head()

Infubinol_pd.rename(columns={"Tumor Volume (mm3)":"Infubinol"}, inplace=True)

# Data set needed for Part 4 bar plot for Drug 2 - Caclulate & store while traversing the Tumor Volume Data 

# Calculate the Original Size, Volume Change for Drug 2
OriginalVolSize = 0
VolumeChange = 0

for index, row in Infubinol_pd.iterrows():
    if (row["Timepoint"] == 0):
        OriginalVolSize = row["Infubinol"]
    
    if (row["Timepoint"] == 45):
        VolumeChange = row["Infubinol"] - OriginalVolSize
        break;

#print ("Original Vol Size: %s Volume Change: %s" %(str(OriginalVolSize), str(VolumeChange)))

#Add the values found into the appropriate columns - Then calculate & store % Volume Change 

for index, row in Tumor_Percent_Change_ByDrug.iterrows():
    if (row["Drug Name"] == "Infubinol"):
        Tumor_Percent_Change_ByDrug.set_value(index, "Original Volume", OriginalVolSize)
        Tumor_Percent_Change_ByDrug.set_value(index, "Volume Change", VolumeChange)
        Tumor_Percent_Change_ByDrug.set_value(index, "% Tumor Volume Change", (VolumeChange / OriginalVolSize) * 100)
        break;

#print (Tumor_Percent_Change_ByDrug.head())

#Infubinol_pd.head()

#clinical_drug_tvol_data = Capmoulin_pd.rename(columns={"Tumor Volume (mm3)":"Capomulin"})
```


```python
# Group By Drugs and Append to the cleaned up list
clinical_ForKetapril = reduced_mouse_drug[reduced_mouse_drug['Drug'] == "Ketapril"].groupby('Timepoint')['Tumor Volume (mm3)'].mean()


Ketapril_pd = pd.DataFrame (clinical_ForKetapril)

Ketapril_pd.reset_index(inplace = True)
Ketapril_pd.head()

Ketapril_pd.rename(columns={"Tumor Volume (mm3)":"Ketapril"}, inplace=True)

# Data set needed for Part 4 bar plot for Drug 3 - Caclulate & store while traversing the Tumor Volume Data 

# Calculate the Original Size, Volume Change for Drug 3
OriginalVolSize = 0
VolumeChange = 0

for index, row in Ketapril_pd.iterrows():
    if (row["Timepoint"] == 0):
        OriginalVolSize = row["Ketapril"]
    
    if (row["Timepoint"] == 45):
        VolumeChange = row["Ketapril"] - OriginalVolSize
        break;

#print ("Original Vol Size: %s Volume Change: %s" %(str(OriginalVolSize), str(VolumeChange)))

#Add the values found into the appropriate columns - Then calculate & store % Volume Change 

for index, row in Tumor_Percent_Change_ByDrug.iterrows():
    if (row["Drug Name"] == "Ketapril"):
        Tumor_Percent_Change_ByDrug.set_value(index, "Original Volume", OriginalVolSize)
        Tumor_Percent_Change_ByDrug.set_value(index, "Volume Change", VolumeChange)
        Tumor_Percent_Change_ByDrug.set_value(index, "% Tumor Volume Change", (VolumeChange / OriginalVolSize) * 100)
        break;

#print (Tumor_Percent_Change_ByDrug.head())

#Ketapril_pd.head()


```


```python
# Group By Drugs and Append to the cleaned up list
clinical_ForPlacebo = reduced_mouse_drug[reduced_mouse_drug['Drug'] == "Placebo"].groupby('Timepoint')['Tumor Volume (mm3)'].mean()


Placebo_pd = pd.DataFrame (clinical_ForPlacebo)

Placebo_pd.reset_index(inplace = True)
Placebo_pd.head()

Placebo_pd.rename(columns={"Tumor Volume (mm3)":"Placebo"}, inplace=True)

# Data set needed for Part 4 bar plot for Drug 4 - Caclulate & store while traversing the Tumor Volume Data 

# Calculate the Original Size, Volume Change for Drug 4
OriginalVolSize = 0
VolumeChange = 0

for index, row in Placebo_pd.iterrows():
    if (row["Timepoint"] == 0):
        OriginalVolSize = row["Placebo"]
    
    if (row["Timepoint"] == 45):
        VolumeChange = row["Placebo"] - OriginalVolSize 
        break;

#print ("Original Vol Size: %s Volume Change: %s" %(str(OriginalVolSize), str(VolumeChange)))

#Add the values found into the appropriate columns - Then calculate & store % Volume Change 

for index, row in Tumor_Percent_Change_ByDrug.iterrows():
    if (row["Drug Name"] == "Placebo"):
        Tumor_Percent_Change_ByDrug.set_value(index, "Original Volume", OriginalVolSize)
        Tumor_Percent_Change_ByDrug.set_value(index, "Volume Change", VolumeChange)
        Tumor_Percent_Change_ByDrug.set_value(index, "% Tumor Volume Change", (VolumeChange / OriginalVolSize) * 100)
        break;

#print (Tumor_Percent_Change_ByDrug.head())


#Placebo_pd.head()


```


```python
#Merge the Different Drug Dataframes by their Timepoints and Gte final dataframe needed to make a scatter plot of 
# Tumor volume change over time 

merged_ForCapInf = pd.merge(Capmoulin_pd , Infubinol_pd, on="Timepoint")

#merged_ForCapInf.head()

merged_ForKetPla = pd.merge(Ketapril_pd , Placebo_pd, on="Timepoint")

#merged_ForKetPla.head()

TumorVol_OverTime = pd.merge(merged_ForCapInf, merged_ForKetPla, on="Timepoint")

#TumorVol_OverTime.head(20)

```


```python
# Try with sns 

#sns.set_style("whitegrid")

#g = sns.lmplot(x='Timepoint', y='Capomulin',data=TumorVol_OverTime)

#sns.lmplot(x='Timepoint', , data=TumorVol_OverTime)
#g.lmplot (x ='Timepoint')
#sns.lmplot(x='Timepoint', y='Infubinol', data=TumorVol_OverTime)

```


```python
# Tell matplotlib to create a scatter plot based upon the above data
Capmoullin = plt.scatter(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Capomulin"], marker="o", facecolors="red", edgecolors="black", label="Capomulin")
Infubinol  = plt.scatter(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Infubinol"], marker="o", facecolors="blue", edgecolors="black", label="Infubinol")
Ketapril = plt.scatter(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Ketapril"], marker="^", facecolors="green", edgecolors="black", label="Ketapril")
Placebo = plt.scatter(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Placebo"], marker="o", facecolors="purple", edgecolors="black", label="Placebo")

# Create a title, x label, and y label for our chart
plt.title("Tumor Response to Treatment")
plt.xlabel("Time (Days)")
plt.ylabel("Tumor Volume (mm3)")

# example error bar values that vary with x-position

plt.errorbar(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Capomulin"], 0.2, color = "r")
plt.errorbar(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Infubinol"], 0.2, color = "b")
plt.errorbar(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Ketapril"], 0.2, color = "g")
plt.errorbar(TumorVol_OverTime["Timepoint"], TumorVol_OverTime["Placebo"], 0.2, color = "k")

#plt.show()

x_max_value = (TumorVol_OverTime["Timepoint"].max())

y_max_value = round(y_max_value)

y_min_value = round (y_min_value)

#print (str(x_max_value))

#print (str(y_max_value))

#print (str(y_min_value))

plt.xlim(0, x_max_value)

plt.ylim( y_min_value-5 , y_max_value + 5)

plt.legend(handles=[Capmoullin, Infubinol, Ketapril, Placebo], loc="best")
plt.grid(color = 'k', linestyle='-.', linewidth=0.5)

plt.show()

```


![png](PharmaAnalyze_files/PharmaAnalyze_12_0.png)



```python
# Part 2: Now for building the data needs for scatter plot of metastatisis over time 

# Take only columns we need from mouse_drug for lot on Tumer volume over Time plot 
#Mouse ID	Timepoint	Tumor Volume (mm3)
reduced_mouse_drug1 = clinical_mouse_drug_data.loc[:, ['Drug','Timepoint','Metastatic Sites']]

reduced_mouse_drug1.head()

# Group By Drugs for Drug 1 Capmoulin 
clinical_ForCapmoulin = reduced_mouse_drug1[reduced_mouse_drug1['Drug'] == "Capomulin"].groupby('Timepoint')['Metastatic Sites'].mean()


Capmoulin_pd = pd.DataFrame (clinical_ForCapmoulin)

Capmoulin_pd.reset_index(inplace = True)
Capmoulin_pd.head()



Capmoulin_pd.rename(columns={"Metastatic Sites":"Capomulin"}, inplace = True)

#drug_tumor_vol = clinical_drug_tvol_data.set_index("Timepoint")

Capmoulin_pd.head()

#Group By Drugs for Drug 2 Infubinol
clinical_ForInfubinol = reduced_mouse_drug1[reduced_mouse_drug1['Drug'] == "Infubinol"].groupby('Timepoint')['Metastatic Sites'].mean()


Infubinol_pd = pd.DataFrame (clinical_ForInfubinol)

Infubinol_pd.reset_index(inplace = True)
Infubinol_pd.head()

Infubinol_pd.rename(columns={"Metastatic Sites":"Infubinol"}, inplace=True)

#Infubinol_pd.head()

```


```python
# Group By Drugs for Drug 3 Ketapril
clinical_ForKetapril = reduced_mouse_drug1[reduced_mouse_drug1['Drug'] == "Ketapril"].groupby('Timepoint')['Metastatic Sites'].mean()


Ketapril_pd = pd.DataFrame (clinical_ForKetapril)

Ketapril_pd.reset_index(inplace = True)
Ketapril_pd.head()

Ketapril_pd.rename(columns={"Metastatic Sites":"Ketapril"}, inplace=True)

#Ketapril_pd.head()

# Group By Drugs for drug 4 Placebo
clinical_ForPlacebo = reduced_mouse_drug1[reduced_mouse_drug1['Drug'] == "Placebo"].groupby('Timepoint')['Metastatic Sites'].mean()


Placebo_pd = pd.DataFrame (clinical_ForPlacebo)

Placebo_pd.reset_index(inplace = True)
Placebo_pd.head()

Placebo_pd.rename(columns={"Metastatic Sites":"Placebo"}, inplace=True)

#Placebo_pd.head()


```


```python
#Merge the Different Drug Dataframes by their Timepoints and Get final dataframe needed to make a scatter plot of 
# Metastatic Sites over time 

merged_ForCapInf = pd.merge(Capmoulin_pd , Infubinol_pd, on="Timepoint")

merged_ForCapInf.head()

merged_ForKetPla = pd.merge(Ketapril_pd , Placebo_pd, on="Timepoint")

merged_ForKetPla.head()

Metastatic_OverTime = pd.merge(merged_ForCapInf, merged_ForKetPla, on="Timepoint")

Metastatic_OverTime.head(20)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Timepoint</th>
      <th>Capomulin</th>
      <th>Infubinol</th>
      <th>Ketapril</th>
      <th>Placebo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
      <td>0.160000</td>
      <td>0.280000</td>
      <td>0.304348</td>
      <td>0.375000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10</td>
      <td>0.320000</td>
      <td>0.666667</td>
      <td>0.590909</td>
      <td>0.833333</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>0.375000</td>
      <td>0.904762</td>
      <td>0.842105</td>
      <td>1.250000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>0.652174</td>
      <td>1.050000</td>
      <td>1.210526</td>
      <td>1.526316</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
      <td>0.818182</td>
      <td>1.277778</td>
      <td>1.631579</td>
      <td>1.941176</td>
    </tr>
    <tr>
      <th>6</th>
      <td>30</td>
      <td>1.090909</td>
      <td>1.588235</td>
      <td>2.055556</td>
      <td>2.266667</td>
    </tr>
    <tr>
      <th>7</th>
      <td>35</td>
      <td>1.181818</td>
      <td>1.666667</td>
      <td>2.294118</td>
      <td>2.642857</td>
    </tr>
    <tr>
      <th>8</th>
      <td>40</td>
      <td>1.380952</td>
      <td>2.100000</td>
      <td>2.733333</td>
      <td>3.166667</td>
    </tr>
    <tr>
      <th>9</th>
      <td>45</td>
      <td>1.476190</td>
      <td>2.111111</td>
      <td>3.363636</td>
      <td>3.272727</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Find ymax and ymin value 

Metastatic_ByDrug = pd.DataFrame(reduced_mouse_drug1.groupby(['Drug','Timepoint'])['Metastatic Sites'].mean())


#Metastatic_ByDrug.head(100)

y_max_value = Metastatic_ByDrug["Metastatic Sites"].max()

y_min_value = Metastatic_ByDrug["Metastatic Sites"].min()

#print ("%s %s" % (str(y_max_value), str(y_min_value)))
```


```python
# Part 2 - Create the Scatter Plot for Metastatic Sites
# Tell matplotlib to create a scatter plot based upon the above data 
Capmoullin = plt.scatter(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Capomulin"], marker="o", facecolors="red", edgecolors="black", label="Capomulin")
Infubinol  = plt.scatter(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Infubinol"], marker="o", facecolors="blue", edgecolors="black", label="Infubinol")
Ketapril = plt.scatter(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Ketapril"], marker="^", facecolors="green", edgecolors="black", label="Ketapril")
Placebo = plt.scatter(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Placebo"], marker="o", facecolors="purple", edgecolors="black", label="Placebo")

# Create a title, x label, and y label for our chart
plt.title("Metastatic Spread During Treatment")
plt.xlabel("Treatment Duration (Days)")
plt.ylabel("Met. Sites")

# example error bar values that vary with x-position
#error = 0.2 * TumorVol_OverTime["Timepoint"]


plt.errorbar(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Capomulin"], 0.2, color = "r")
plt.errorbar(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Infubinol"], 0.2, color = "b")
plt.errorbar(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Ketapril"], 0.2, color = "g")
plt.errorbar(Metastatic_OverTime["Timepoint"], Metastatic_OverTime["Placebo"], 0.2, color = "k")

#plt.show()

#ax.grid(color='r', linestyle='-', linewidth=2)
x_max_value = (Metastatic_OverTime["Timepoint"].max())

y_max_value = round(y_max_value)

y_min_value = round (y_min_value)

#print (str(x_max_value))

#print (str(y_max_value))

#print (str(y_min_value))

plt.xlim(0, x_max_value)

plt.ylim( y_min_value - 0.5 , y_max_value +  0.5 )

plt.legend(handles=[Capmoullin, Infubinol, Ketapril, Placebo], loc="best")
plt.grid(color = 'k', linestyle='-.', linewidth=0.5)

plt.show()


```


![png](PharmaAnalyze_files/PharmaAnalyze_17_0.png)



```python
# Part 3: Now for building the data needs for scatter plot of Survival Rate over time 

# Take only columns we need from mouse_drug for lot on Tumer volume over Time plot 
#Mouse ID	Timepoint	Tumor Volume (mm3)
reduced_mouse_drug2 = clinical_mouse_drug_data.loc[:, ['Drug','Timepoint','Mouse ID']]

#reduced_mouse_drug2.head()

# Group By Drugs for Drug 1 Capmoulin and count number of mice 
clinical_ForCapmoulin = reduced_mouse_drug2[reduced_mouse_drug2['Drug'] == "Capomulin"].groupby('Timepoint')['Mouse ID'].count()

Capmoulin_pd = pd.DataFrame (clinical_ForCapmoulin)

Capmoulin_pd.reset_index(inplace = True)

Capmoulin_pd.rename(columns={"Mouse ID":"Capomulin"}, inplace = True)


#Need to calculate Survival Rate %
Total_MouseCount = 0

for index, row in Capmoulin_pd.iterrows():
    if (row["Timepoint"] == 0):
        Total_MouseCount = row["Capomulin"]
        break; 

#print (str(Total_MouseCount))

Capmoulin_pd["Capomulin Survival Rate %"] = Capmoulin_pd["Capomulin"] / Total_MouseCount * 100

Capmoulin_pd.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Timepoint</th>
      <th>Capomulin</th>
      <th>Capomulin Survival Rate %</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>25</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
      <td>25</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10</td>
      <td>25</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>24</td>
      <td>96.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>23</td>
      <td>92.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Group By Drugs for Drug 2 Infubinol
clinical_ForInfubinol = reduced_mouse_drug2[reduced_mouse_drug2['Drug'] == "Infubinol"].groupby('Timepoint')['Mouse ID'].count()


Infubinol_pd = pd.DataFrame (clinical_ForInfubinol)

Infubinol_pd.reset_index(inplace = True)


Infubinol_pd.rename(columns={"Mouse ID":"Infubinol"}, inplace=True)

#Need to calculate Survival Rate %
Total_MouseCount = 0

for index, row in Infubinol_pd.iterrows():
    if (row["Timepoint"] == 0):
        Total_MouseCount = row["Infubinol"]
        break; 

print (str(Total_MouseCount))

Infubinol_pd["Infubinol Survival Rate %"] = Infubinol_pd["Infubinol"] / Total_MouseCount * 100

#Infubinol_pd.head()
```

    25



```python
# Group By Drugs for Drug 3 Ketapril
clinical_ForKetapril = reduced_mouse_drug2[reduced_mouse_drug2['Drug'] == "Ketapril"].groupby('Timepoint')['Mouse ID'].count()


Ketapril_pd = pd.DataFrame (clinical_ForKetapril)

Ketapril_pd.reset_index(inplace = True)
Ketapril_pd.head()

Ketapril_pd.rename(columns={"Mouse ID":"Ketapril"}, inplace=True)

#Need to calculate Survival Rate %
Total_MouseCount = 0

for index, row in Ketapril_pd.iterrows():
    if (row["Timepoint"] == 0):
        Total_MouseCount = row["Ketapril"]
        break; 

print (str(Total_MouseCount))

Ketapril_pd["Ketapril Survival Rate %"] = Ketapril_pd["Ketapril"] / Total_MouseCount * 100


#Ketapril_pd.head()


```

    25



```python
# Group By Drugs for drug 4 Placebo
clinical_ForPlacebo = reduced_mouse_drug2[reduced_mouse_drug2['Drug'] == "Placebo"].groupby('Timepoint')['Mouse ID'].count()


Placebo_pd = pd.DataFrame (clinical_ForPlacebo)

Placebo_pd.reset_index(inplace = True)
Placebo_pd.head()

Placebo_pd.rename(columns={"Mouse ID":"Placebo"}, inplace=True)

#Need to calculate Survival Rate %
Total_MouseCount = 0

for index, row in Placebo_pd.iterrows():
    if (row["Timepoint"] == 0):
        Total_MouseCount = row["Placebo"]
        break; 

#print (str(Total_MouseCount))

Placebo_pd["Placebo Survival Rate %"] = Placebo_pd["Placebo"] / Total_MouseCount * 100

#Placebo_pd.head()


```


```python
#Merge the Different Drug Dataframes by their Timepoints and Get final dataframe needed to make a scatter plot of 
# Survival rate  over time 

merged_ForCapInf = pd.merge(Capmoulin_pd , Infubinol_pd, on="Timepoint")

#merged_ForCapInf.head()

merged_ForKetPla = pd.merge(Ketapril_pd , Placebo_pd, on="Timepoint")

#merged_ForKetPla.head()

SurvivalRate_OverTime = pd.merge(merged_ForCapInf, merged_ForKetPla, on="Timepoint")

SurvivalRate_OverTime.head(20)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Timepoint</th>
      <th>Capomulin</th>
      <th>Capomulin Survival Rate %</th>
      <th>Infubinol</th>
      <th>Infubinol Survival Rate %</th>
      <th>Ketapril</th>
      <th>Ketapril Survival Rate %</th>
      <th>Placebo</th>
      <th>Placebo Survival Rate %</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>25</td>
      <td>100.0</td>
      <td>25</td>
      <td>100.0</td>
      <td>25</td>
      <td>100.0</td>
      <td>25</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
      <td>25</td>
      <td>100.0</td>
      <td>25</td>
      <td>100.0</td>
      <td>23</td>
      <td>92.0</td>
      <td>24</td>
      <td>96.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10</td>
      <td>25</td>
      <td>100.0</td>
      <td>21</td>
      <td>84.0</td>
      <td>22</td>
      <td>88.0</td>
      <td>24</td>
      <td>96.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>15</td>
      <td>24</td>
      <td>96.0</td>
      <td>21</td>
      <td>84.0</td>
      <td>19</td>
      <td>76.0</td>
      <td>20</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>23</td>
      <td>92.0</td>
      <td>20</td>
      <td>80.0</td>
      <td>19</td>
      <td>76.0</td>
      <td>19</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
      <td>22</td>
      <td>88.0</td>
      <td>18</td>
      <td>72.0</td>
      <td>19</td>
      <td>76.0</td>
      <td>17</td>
      <td>68.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>30</td>
      <td>22</td>
      <td>88.0</td>
      <td>17</td>
      <td>68.0</td>
      <td>18</td>
      <td>72.0</td>
      <td>15</td>
      <td>60.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>35</td>
      <td>22</td>
      <td>88.0</td>
      <td>12</td>
      <td>48.0</td>
      <td>17</td>
      <td>68.0</td>
      <td>14</td>
      <td>56.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>40</td>
      <td>21</td>
      <td>84.0</td>
      <td>10</td>
      <td>40.0</td>
      <td>15</td>
      <td>60.0</td>
      <td>12</td>
      <td>48.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>45</td>
      <td>21</td>
      <td>84.0</td>
      <td>9</td>
      <td>36.0</td>
      <td>11</td>
      <td>44.0</td>
      <td>11</td>
      <td>44.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Find ymax and ymin value 

SurvivalRate_ByDrug = pd.DataFrame(reduced_mouse_drug2.groupby(['Drug','Timepoint'])['Mouse ID'].count())

SurvivalRate_ByDrug.head(100)

y_max_value = SurvivalRate_OverTime["Capomulin Survival Rate %"].max()

#Assign the y-max value appropriately 
if (SurvivalRate_OverTime["Infubinol Survival Rate %"].max() > y_max_value):
    y_max_value = SurvivalRate_OverTime["Infubinol Survival Rate %"].max()

if (SurvivalRate_OverTime["Ketapril Survival Rate %"].max() > y_max_value):
     y_max_value = SurvivalRate_OverTime["Ketapril Survival Rate %"].max()

if (SurvivalRate_OverTime["Placebo Survival Rate %"].max() > y_max_value):
     y_max_value = SurvivalRate_OverTime["Placebo Survival Rate %"].max()

#Assign the y-min value appropritaley 
y_min_value = SurvivalRate_OverTime["Capomulin Survival Rate %"].min()

if (SurvivalRate_OverTime["Infubinol Survival Rate %"].min() < y_min_value):
    y_min_value = SurvivalRate_OverTime["Infubinol Survival Rate %"].min()

if (SurvivalRate_OverTime["Ketapril Survival Rate %"].min() < y_min_value):
     y_min_value = SurvivalRate_OverTime["Ketapril Survival Rate %"].min()

if (SurvivalRate_OverTime["Placebo Survival Rate %"].min() < y_min_value):
     y_min_value = SurvivalRate_OverTime["Placebo Survival Rate %"].min()

#print ("%s %s" % (str(y_max_value), str(y_min_value)))

#print ("%s" % (str(x_max_value)))
```


```python
# Part 3 - Create the Scatter Plot for Survival Rate 
# Tell matplotlib to create a scatter plot based upon the above data 
Capmoullin = plt.scatter(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Capomulin Survival Rate %"], marker="o", facecolors="red", edgecolors="black", label="Capomulin")
Infubinol  = plt.scatter(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Infubinol Survival Rate %"], marker="o", facecolors="blue", edgecolors="black", label="Infubinol")
Ketapril = plt.scatter(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Ketapril Survival Rate %"], marker="^", facecolors="green", edgecolors="black", label="Ketapril")
Placebo = plt.scatter(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Placebo Survival Rate %"], marker="o", facecolors="purple", edgecolors="black", label="Placebo")

# Create a title, x label, and y label for our chart
plt.title("Survival During Treatment")
plt.xlabel("Time (Days)")
plt.ylabel("Survival Rate (%)")

# example error bar values that vary with x-position
#error = 0.2 * TumorVol_OverTime["Timepoint"]


plt.errorbar(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Capomulin Survival Rate %"], 0.2, color = "r")
plt.errorbar(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Infubinol Survival Rate %"], 0.2, color = "b")
plt.errorbar(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Ketapril Survival Rate %"], 0.2, color = "g")
plt.errorbar(SurvivalRate_OverTime["Timepoint"], SurvivalRate_OverTime["Placebo Survival Rate %"], 0.2, color = "k")

#plt.show()

#ax.grid(color='r', linestyle='-', linewidth=2)
x_max_value = (SurvivalRate_OverTime["Timepoint"].max())

y_max_value = round(y_max_value)

y_min_value = round (y_min_value)

#print (str(x_max_value))

#print (str(y_max_value))

#print (str(y_min_value))

plt.xlim(0, x_max_value)

plt.ylim( y_min_value - 5 , y_max_value +  5 )

plt.legend(handles=[Capmoullin, Infubinol, Ketapril, Placebo], loc="best")
plt.grid(color = 'k', linestyle='-.', linewidth=0.5)

plt.show()




```


![png](PharmaAnalyze_files/PharmaAnalyze_24_0.png)



```python
# Part 4 - Bar plot showing the % Tumor Volume growth or reduction in Bar plots 

#To do this - Pull up the data we have calculated to show this Bar plot so far 

Tumor_Percent_Change_ByDrug.head()

Tumor_Percent_Change_ByDrug["Color"] = ""
green_color = 'g'
red_color = 'r'

for index, row in Tumor_Percent_Change_ByDrug.iterrows():
    # If the Tumor size has decreased, this is a positive and it would need reflected as green in bar plot else red
    if (row["% Tumor Volume Change"] <= 0):
        Tumor_Percent_Change_ByDrug.set_value(index, "Color", green_color)
    else:
        Tumor_Percent_Change_ByDrug.set_value(index, "Color", red_color)

Tumor_Percent_Change_ByDrug.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Drug Name</th>
      <th>Original Volume</th>
      <th>Volume Change</th>
      <th>% Tumor Volume Change</th>
      <th>Color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Capomulin</td>
      <td>45</td>
      <td>-8.76389</td>
      <td>-19.4753</td>
      <td>g</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Infubinol</td>
      <td>45</td>
      <td>20.7556</td>
      <td>46.1235</td>
      <td>r</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ketapril</td>
      <td>45</td>
      <td>25.663</td>
      <td>57.0288</td>
      <td>r</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Placebo</td>
      <td>45</td>
      <td>23.0841</td>
      <td>51.298</td>
      <td>r</td>
    </tr>
  </tbody>
</table>
</div>




```python
def autolabel(rects, ax):
    # Get y-axis height to calculate label position from.
    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom
    #half_y_height = round(y_height/2)
    
    for rect in rects:
        height = rect.get_height()
        
        # Fraction of axis height taken up by this rectangle
        p_height = (height / y_height)
        
        # If we can fit the label above the column, do that;
        # otherwise, put it inside the column.
        #if height < 0 and goes dowm,we need to write it below 0versus above 0
        if height < 0: # arbitrary; 95% looked good to me.
            label_position = ((rect.get_x() + rect.get_width()/2.) - 8)
        else:
            label_position = ((rect.get_x() + rect.get_width()/2.) + 2)
        
        ax.text(rect.get_x() + rect.get_width()/2., label_position, '%d%%' % int(height), ha='center', va='bottom')


```


```python
# Create a title, x label, and y label for our chart
plt.title("Tumor Change Over 45 Day Treatment")
plt.xlabel("Drug Name")
plt.ylabel("% Tumor Volume Change")

x_axis = np.arange(len(Tumor_Percent_Change_ByDrug["Drug Name"]))

#print (x_axis)

#fig, ax = plt.subplots()
rect1 = plt.bar(x_axis, Tumor_Percent_Change_ByDrug["% Tumor Volume Change"], color= Tumor_Percent_Change_ByDrug["Color"], alpha=0.5, align="edge")

# Tell matplotlib where we would like to place each of our x axis headers
tick_locations = [value+0.4 for value in x_axis]
plt.xticks(tick_locations, Tumor_Percent_Change_ByDrug["Drug Name"])

# Count Plot (a.k.a. Bar Plot)
#sns.countplot(x='Drug Name', data=Tumor_Percent_Change_ByDrug["% Tumor Volume Change"])
 
# Rotate x-labels
#plt.xticks(rotation=-45)


y_max_value = round(Tumor_Percent_Change_ByDrug["% Tumor Volume Change"].max())

y_min_value = round (Tumor_Percent_Change_ByDrug["% Tumor Volume Change"].min())

#print ("X Max: %s Y Max: %s Y Min: %s" %(str(len(x_axis)), str(y_max_value), str(y_min_value)))

plt.xlim(-0.25, len(x_axis))

plt.ylim( y_min_value - 5 , y_max_value +  5 )


plt.grid(color = 'k', linestyle='-.', linewidth=0.5)



autolabel(rect1, plt.gca())

plt.show()
```


![png](PharmaAnalyze_files/PharmaAnalyze_27_0.png)

