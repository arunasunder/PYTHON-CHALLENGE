

```python
# City School Analysis - Written by Aruna Amaresan 
# Date: Dec 07 - Dec 09th 2017
# For slicing and dicing All Schools in Districts, Do School Performance Analysis Data 
# Assumptions: For Math:    The pass mark is calculated for 60 and above 
#              For Reading: The pass mark is calculated for 65 and above 
# Input: The sources CSV files are expected to be kept in the raw_data folder - one for student and other for school
# 
# Output: 9 different reports are generated: - District Summary 
#                                            - School Summary ( Aggregated within each School)
#                                            - Top 5 Performing Schools by % Overall Passing Rate ( Aggregated within each School)     
#                                            - Bottom 5 Performing Schools by % Overall Passing Rate ( Aggregated within each School)
#                                            - Math Score (Averages) by Grade
#                                            - Reading Score (Averages) by Grade - 9th to 12th 
#                                            - Performances by School Spending 
#                                            - Performances by School Size
#                                            - Performances by School Type

# Import Dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os 
```


```python
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

#print (color.BOLD + 'Hello World !' + color.END)
```


```python
# load CSV files 
schoolsCSV = os.path.join('raw_data', 'schools_complete.csv')

schools_pd = pd.read_csv(schoolsCSV, encoding="iso-8859-1", low_memory=False)
#schools_pd.head(20)
```


```python
#Load Student CSV file 
studentsCSV = os.path.join('raw_data', 'students_complete.csv')

students_pd = pd.read_csv(studentsCSV, encoding="iso-8859-1", low_memory=False)
#students_pd.head()
```


```python
#cleanse of any empty rows in students
#students_pd.columns
students = students_pd.dropna(how="any")
#students.head()
```


```python
#Clean up any rows with empty values in schools data
school_count = schools_pd.dropna(how="any")

#school_count.head()
```


```python
#school_count.columns
#students.columns
```


```python
#Get Total Number of school 
NumberOfSchools = len(school_count)
#print(NumberOfSchools)


#get Total number of students 
TotalStudents = school_count['size'].sum()
#print(TotalStudents)

#Get Total Budget
TotalBudget = school_count['budget'].sum()
#print(TotalBudget)
```


```python
#student_schoolcount = students_pd["school"].value_counts()
#student_schoolcount

#Find average math score 
average_MathScore = students["math_score"].mean()
#print(average_MathScore)

#Find average reading score 
average_ReadingScore = students["reading_score"].mean()
#print(average_ReadingScore)

#Lets assume a passing score is 60 and above for Math 
passed_math = students.loc[students["math_score"] >= 60]
#passed_math.head()

#Find Percent of Students who had passed math
passed_math_count = passed_math["name"].count()
#print(passed_math_count)

#For reading calculate the same - Lets assume a passing rate of 65 for reading
passed_reading = students.loc[students["reading_score"] >= 65]
#print(passed_reading.head())

#Find Percent of Students who had passed math
passed_reading_count = passed_reading["name"].count()
#print(passed_reading_count)
```


```python
# Calculate percentage of students passign math and similarly for reading . Then calculate overall percentage 
math_percent = (passed_math_count/TotalStudents) * 100
#print(math_percent)
reading_percent = (passed_reading_count/TotalStudents) * 100
#print(reading_percent)

overall_passing_rate = ((math_percent + reading_percent)/2) 
#print( overall_passing_rate )
#print(f" % Male: {male_percent}\n % Female: {female_percent}\n % non_specifc: {non_gender_specific}")
```


```python
# Create a new table consolodating above calculations
district_summary = pd.DataFrame({"Total Schools": [NumberOfSchools],
                                   "Total Students": [TotalStudents],
                                   "Total Budget": [TotalBudget],
                                   "Average Math Score": [average_MathScore],
                                   "Average Reading Score": [average_ReadingScore],
                                   "% Passing Math":[math_percent],
                                   "% Passing Reading":[reading_percent],
                                   "% Overall Passing Rate": [ overall_passing_rate ]
})
district_summary  = district_summary [["Total Schools",
                                   "Total Students",
                                   "Total Budget",
                                   "Average Math Score",
                                   "Average Reading Score",
                                   "% Passing Math",
                                   "% Passing Reading",
                                   "% Overall Passing Rate"]]

district_summary  = district_summary.round(2)

#district_summary 
```


```python
# Formatting to be done to certain columns as per sample PDF shown 
district_summary["Total Students"] = district_summary["Total Students"].map("{0:,.0f}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${0:,.2f}".format)
print (color.BOLD + 'District Summary' + color.END)
print ('****************')
district_summary
#district_summary.dtypes
```

    [1mDistrict Summary[0m
    ****************





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
      <th>Total Schools</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15</td>
      <td>39,170</td>
      <td>$24,649,428.00</td>
      <td>78.99</td>
      <td>81.88</td>
      <td>92.45</td>
      <td>96.2</td>
      <td>94.32</td>
    </tr>
  </tbody>
</table>
</div>




```python
#For School Summary 

# Take only columns we need from school_count
reduced_school_count = school_count.loc[:, ['name','type','size', 'budget']]
#reduced_school_count.head()
```


```python
reduced_school_count = reduced_school_count.rename(columns={"name":"school", 
                                                            "type":"School Type", 
                                                            "size":"Total Students", 
                                                            "budget":"Total School Budget",
                                                                 })
#reduced_school_count

#Store data for binning on School Size and School Type
School_Size_Type_Performance = pd.DataFrame(reduced_school_count)

```


```python
# Calculate percentage of eac bootcamp's students who are recommenders
reduced_school_count["Per Student Budget"] = reduced_school_count["Total School Budget"] / reduced_school_count["Total Students"]

#reduced_school_count.head()
```


```python
# Take only columns we need from school_count
#name	gender	grade	school	reading_score	math_score
reduced_student_columns = students.loc[:, ['school','reading_score', 'math_score']]
#reduced_student_columns.head()


```


```python
# Group By Schools and Find Average reading score
AverageMathScore_BySchool = pd.DataFrame(reduced_student_columns.groupby("school")["math_score"].mean())

AverageMathScore_BySchool.reset_index(inplace=True)
AverageMathScore_BySchool.columns=["school", "Average Math Score"]

#AverageMathScore_BySchool.head()
```


```python
# Create a groupby variable that groups preTestScores by regiment
#groupby_schools = students['reading_score'].groupby(students['school'])
#groupby_schools.mean()

# Group By Schools and Find Average reading score
AverageReadingScore_BySchool = pd.DataFrame(reduced_student_columns.groupby("school")["reading_score"].mean())

AverageReadingScore_BySchool.reset_index(inplace=True)
AverageReadingScore_BySchool.columns=["school", "Average Reading Score"]

#AverageReadingScore_BySchool.head()
```


```python
# Merge the two created data frames on the name of tbe school
merged_scores = pd.merge(AverageMathScore_BySchool , AverageReadingScore_BySchool, on="school")
#merged_scores.head()

#Students_InEachSchool = reduced_student_columns["school"].value_counts()
#Students_InEachSchool
```


```python
# The pass score for Math is always assumed to be 60 and
# the pass score for reading is always taken at 65

# Group By Schools and Find Pass Math Count 
BySchool_MathPass = reduced_student_columns[reduced_student_columns['math_score'] >= 60].groupby('school')['math_score'].count()

#Group_BySchool = reduced_student_columns.groupby(["school"])  #grouped_usa_df = usa_ufo_df.groupby(["state"])
BySchool_MathPassCount = pd.DataFrame (BySchool_MathPass)
BySchool_MathPassCount.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
#BySchool_MathPassCount.columns = ["school", "Math Pass Count "]
#BySchool_MathPassCount.head()

```


```python
#Now find the Reading Pass Count 
BySchool_ReadPass = reduced_student_columns[reduced_student_columns['reading_score'] >= 65].groupby('school')['reading_score'].count()

#Group_BySchool = reduced_student_columns.groupby(["school"])  
BySchool_ReadPassCount = pd.DataFrame (BySchool_ReadPass)
BySchool_ReadPassCount.reset_index(level = 0, inplace = True) # Ensure we make the index also a column 

#BySchool_ReadPassCount.head()

```


```python
#Merge the Pass Data Frames on the name of school
merged_PassCount = pd.merge(BySchool_MathPassCount , BySchool_ReadPassCount, on="school")
#merged_PassCount.head()
```


```python
#Merge the Score and Pass Data Frames on the name of school
merged_Scores_PassCount = pd.merge(merged_scores , merged_PassCount, on="school")
#merged_Scores_PassCount.head()
```


```python
merged_school_studentData = pd.merge(reduced_school_count , merged_Scores_PassCount, on="school")
#merged_school_studentData.head()
```


```python
# Calculate percentage of Math Pass Rate and add to column 
merged_school_studentData["% Passing Math"] = merged_school_studentData["math_score"] / merged_school_studentData["Total Students"] * 100

# Sort results in descending order
#merged_df = merged_df.sort_values(["% Recommend"], ascending=False).round(2)

#merged_school_studentData.head()
```


```python
# Calculate percentage of Math Pass Rate and add to column 
merged_school_studentData["% Passing Reading"] = merged_school_studentData["reading_score"] / merged_school_studentData["Total Students"] * 100

# Sort results in descending order
#merged_df = merged_df.sort_values(["% Recommend"], ascending=False).round(2)


#merged_school_studentData.head()
```


```python
# Calculate percentage of Math Pass Rate and add to column 
merged_school_studentData["% Overall Passing Rate"] = (merged_school_studentData["% Passing Math"] + merged_school_studentData["% Passing Reading"]) / 2
#merged_school_studentData.dtypes

#Store data away for Binning Exercises 
PerStudentSpending_BySchool = pd.DataFrame(merged_school_studentData)

merged_school_studentData.drop(['math_score'], axis = 1, inplace = True)
merged_school_studentData.drop(['reading_score'], axis = 1, inplace = True)


#For Display of the values - store in a sperate Data Frame
display_school_studentData = pd.DataFrame(merged_school_studentData)

# Format for $ values for the Budget columns
display_school_studentData["Per Student Budget"] = display_school_studentData["Per Student Budget"].map("${0:,.2f}".format)
display_school_studentData["Total School Budget"] = display_school_studentData["Total School Budget"].map("${0:,.2f}".format)


# Format for percentages

display_school_studentData = display_school_studentData.rename(columns={"school":""})
#display_school_studentData.head()

display_school_studentData["% Passing Reading"] = display_school_studentData["% Passing Reading"].map("{0:,.2f}%".format)
# Format for percentages
display_school_studentData["% Passing Math"] = display_school_studentData["% Passing Math"].map("{0:,.2f}%".format)

display_school_studentData["% Overall Passing Rate"] = display_school_studentData["% Overall Passing Rate"].map("{0:,.2f}%".format)


print (color.BOLD + "School Summary" + color.END)
print ("***************")
display_school_studentData


#merged_school_studentData.head()



#Drop the unneded columns and pill in only what u need for School Summary 
#final_students_data = merged_school_studentData.iloc[:,[0,1,2,3,4,5,6,9,10,11]]

#final_students_data.reset_index(level=0, inplace=True)
#final_students_data.head()
```

    [1mSchool Summary[0m
    ***************





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
      <th></th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>$1,910,635.00</td>
      <td>$655.00</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>88.86%</td>
      <td>94.48%</td>
      <td>91.67%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Figueroa High School</td>
      <td>District</td>
      <td>2949</td>
      <td>$1,884,411.00</td>
      <td>$639.00</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>88.44%</td>
      <td>94.54%</td>
      <td>91.49%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Shelton High School</td>
      <td>Charter</td>
      <td>1761</td>
      <td>$1,056,600.00</td>
      <td>$600.00</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Hernandez High School</td>
      <td>District</td>
      <td>4635</td>
      <td>$3,022,020.00</td>
      <td>$652.00</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>89.08%</td>
      <td>94.61%</td>
      <td>91.84%</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>Charter</td>
      <td>1468</td>
      <td>$917,500.00</td>
      <td>$625.00</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Wilson High School</td>
      <td>Charter</td>
      <td>2283</td>
      <td>$1,319,574.00</td>
      <td>$578.00</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Cabrera High School</td>
      <td>Charter</td>
      <td>1858</td>
      <td>$1,081,356.00</td>
      <td>$582.00</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Bailey High School</td>
      <td>District</td>
      <td>4976</td>
      <td>$3,124,928.00</td>
      <td>$628.00</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>89.53%</td>
      <td>94.55%</td>
      <td>92.04%</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Holden High School</td>
      <td>Charter</td>
      <td>427</td>
      <td>$248,087.00</td>
      <td>$581.00</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>Charter</td>
      <td>962</td>
      <td>$585,858.00</td>
      <td>$609.00</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Wright High School</td>
      <td>Charter</td>
      <td>1800</td>
      <td>$1,049,400.00</td>
      <td>$583.00</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Rodriguez High School</td>
      <td>District</td>
      <td>3999</td>
      <td>$2,547,363.00</td>
      <td>$637.00</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>88.55%</td>
      <td>94.62%</td>
      <td>91.59%</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Johnson High School</td>
      <td>District</td>
      <td>4761</td>
      <td>$3,094,650.00</td>
      <td>$650.00</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>89.18%</td>
      <td>94.48%</td>
      <td>91.83%</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Ford High School</td>
      <td>District</td>
      <td>2739</td>
      <td>$1,763,916.00</td>
      <td>$644.00</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>89.30%</td>
      <td>93.87%</td>
      <td>91.58%</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Thomas High School</td>
      <td>Charter</td>
      <td>1635</td>
      <td>$1,043,130.00</td>
      <td>$638.00</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.00%</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Display top 5 entries 
#merged_school_studentData["% Overall Passing Rate"] = pd.to_numeric(merged_school_studentData["% Overall Passing Rate"])

#Get Data for Top 5 and botttom 5 performing schools - Sort results in descending order
#sorted_by_PassRate = 

#sorted_by_PassRate.head()

sorted_by_PassRate = merged_school_studentData.sort_values("% Overall Passing Rate", ascending = False).round(2)

sorted_by_PassRate.set_index('school', inplace = True)

sorted_by_PassRate = sorted_by_PassRate.rename(index={'school':''})
sorted_by_PassRate

top_performing_header = 'Top Performing Schools (By Passing Rate)\n'
print (color.BOLD + top_performing_header + color.END)
print('*****************************************')

display_Top5PassRate = sorted_by_PassRate.iloc[0:5,:]

# Format for $ values for the Budget columns
#display_Top5PassRate["Per Student Budget"] = display_Top5PassRate["Per Student Budget"].map("${0:,.2f}".format)
#display_Top5PassRate["Total School Budget"] = display_Top5PassRate["Total School Budget"].map("${0:,.2f}".format)


display_Top5PassRate
#sorted_by_PassRate = merged_school_studentData.sort_values("% Overall Passing Rate"", ascending=False)
#sorted_by_PassRate.head()
```

    [1mTop Performing Schools (By Passing Rate)
    [0m
    *****************************************





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
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>$1,056,600.00</td>
      <td>$600.00</td>
      <td>83.36</td>
      <td>83.73</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>$917,500.00</td>
      <td>$625.00</td>
      <td>83.35</td>
      <td>83.82</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>$1,319,574.00</td>
      <td>$578.00</td>
      <td>83.27</td>
      <td>83.99</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>$1,081,356.00</td>
      <td>$582.00</td>
      <td>83.06</td>
      <td>83.98</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>$248,087.00</td>
      <td>$581.00</td>
      <td>83.80</td>
      <td>83.81</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#sorted_by_PassRate.columns

sorted_by_PassRate = merged_school_studentData.sort_values("% Overall Passing Rate", ascending = True).round(2)

sorted_by_PassRate.set_index('school', inplace = True)

sorted_by_PassRate = sorted_by_PassRate.rename(index={'school':''})
#sorted_by_PassRate

bottom_performing_header = 'Bottom Performing Schools (By Passing Rate)\n'
print (color.BOLD + bottom_performing_header + color.END)
print('********************************************')

#get Last 5 rows of dataframe to Display Bottom performing Schools by passing rate 
display_Bottom5PassRate = sorted_by_PassRate.iloc[0:5,:] 
display_Bottom5PassRate
```

    [1mBottom Performing Schools (By Passing Rate)
    [0m
    ********************************************





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
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>$1,884,411.00</td>
      <td>$639.00</td>
      <td>76.71</td>
      <td>81.16</td>
      <td>88.44</td>
      <td>94.54</td>
      <td>91.49</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>$1,763,916.00</td>
      <td>$644.00</td>
      <td>77.10</td>
      <td>80.75</td>
      <td>89.30</td>
      <td>93.87</td>
      <td>91.58</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>$2,547,363.00</td>
      <td>$637.00</td>
      <td>76.84</td>
      <td>80.74</td>
      <td>88.55</td>
      <td>94.62</td>
      <td>91.59</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>$1,910,635.00</td>
      <td>$655.00</td>
      <td>76.63</td>
      <td>81.18</td>
      <td>88.86</td>
      <td>94.48</td>
      <td>91.67</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>$3,094,650.00</td>
      <td>$650.00</td>
      <td>77.07</td>
      <td>80.97</td>
      <td>89.18</td>
      <td>94.48</td>
      <td>91.83</td>
    </tr>
  </tbody>
</table>
</div>




```python
# For Math Scrores (Average) By Grade 
#name	gender	grade	school	reading_score	math_score 
reduced_student_mathcolumns = students.loc[:, ['school','grade', 'math_score']]
#reduced_student_mathcolumns.columns
#reduced_student_mathcolumns.dtypes

#MathScore_ByGradeSchool = pd.DataFrame(reduced_student_mathcolumns.groupby(["school", "grade"])["math_score"].mean())
#MathScore_ByGradeSchool

#unique = reduced_student_mathcolumns["grade"].unique()
#unique
```


```python
#Get 9th grade Average Math score by School 
Stu_9thGrade_Math = reduced_student_mathcolumns[reduced_student_mathcolumns['grade'] == '9th'].groupby('school')['math_score'].mean()
Stu_9thGrade_MathAvg = pd.DataFrame (Stu_9thGrade_Math)
Stu_9thGrade_MathAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_9thGrade_MathAvg = Stu_9thGrade_MathAvg.rename(columns={"math_score":"9th"})
#Stu_9thGrade_MathAvg.head()

```


```python
#Get 10th grade Average Math score by School 
Stu_10thGrade_Math = reduced_student_mathcolumns[reduced_student_mathcolumns['grade'] == '10th'].groupby('school')['math_score'].mean()
Stu_10thGrade_MathAvg = pd.DataFrame (Stu_10thGrade_Math)

Stu_10thGrade_MathAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_10thGrade_MathAvg = Stu_10thGrade_MathAvg.rename(columns={"math_score":"10th"})
#Stu_10thGrade_MathAvg.head()


```


```python
#Get 11th grade Average Math score by School 
Stu_11thGrade_Math = reduced_student_mathcolumns[reduced_student_mathcolumns['grade'] == '11th'].groupby('school')['math_score'].mean()
Stu_11thGrade_MathAvg = pd.DataFrame (Stu_11thGrade_Math)

Stu_11thGrade_MathAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_11thGrade_MathAvg = Stu_11thGrade_MathAvg.rename(columns={"math_score":"11th"})
#Stu_11thGrade_MathAvg.head()
```


```python
#Get 12th grade Average Math score by School 
Stu_12thGrade_Math = reduced_student_mathcolumns[reduced_student_mathcolumns['grade'] == '12th'].groupby('school')['math_score'].mean()
Stu_12thGrade_MathAvg = pd.DataFrame (Stu_12thGrade_Math)

Stu_12thGrade_MathAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_12thGrade_MathAvg = Stu_12thGrade_MathAvg.rename(columns={"math_score":"12th"})
#Stu_12thGrade_MathAvg.head()
```


```python
#Merge all the 9th 10h 11th and 12th average Math grade by school into one table 
merged_9th_10th_AvgMathScore = pd.merge(Stu_9thGrade_MathAvg , Stu_10thGrade_MathAvg, on="school")

merged_9th_10th_11thAvgMathScore = pd.merge(merged_9th_10th_AvgMathScore , Stu_11thGrade_MathAvg, on="school")

merged_9th_10th_11th_12thAvgMathScore = pd.merge(merged_9th_10th_11thAvgMathScore , Stu_12thGrade_MathAvg, on="school")

#merged_9th_10th_11th_12thAvgMathScore.head()
```


```python
#Update displays to show in form of table 
display_AvgMathScore_BySchoolGrade = merged_9th_10th_11th_12thAvgMathScore
MathGrade_header ="Math Scores By Grade"

display_AvgMathScore_BySchoolGrade = display_AvgMathScore_BySchoolGrade.rename(columns={'school':''})

print (color.BOLD + MathGrade_header + color.END)
print('**********************')
display_AvgMathScore_BySchoolGrade
```

    [1mMath Scores By Grade[0m
    **********************





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
      <th></th>
      <th>9th</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.083676</td>
      <td>76.996772</td>
      <td>77.515588</td>
      <td>76.492218</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.094697</td>
      <td>83.154506</td>
      <td>82.765560</td>
      <td>83.277487</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.403037</td>
      <td>76.539974</td>
      <td>76.884344</td>
      <td>77.151369</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.361345</td>
      <td>77.672316</td>
      <td>76.918058</td>
      <td>76.179963</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>82.044010</td>
      <td>84.229064</td>
      <td>83.842105</td>
      <td>83.356164</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.438495</td>
      <td>77.337408</td>
      <td>77.136029</td>
      <td>77.186567</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.787402</td>
      <td>83.429825</td>
      <td>85.000000</td>
      <td>82.855422</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>77.027251</td>
      <td>75.908735</td>
      <td>76.446602</td>
      <td>77.225641</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.187857</td>
      <td>76.691117</td>
      <td>77.491653</td>
      <td>76.863248</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.625455</td>
      <td>83.372000</td>
      <td>84.328125</td>
      <td>84.121547</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.859966</td>
      <td>76.612500</td>
      <td>76.395626</td>
      <td>77.690748</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.420755</td>
      <td>82.917411</td>
      <td>83.383495</td>
      <td>83.778976</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.590022</td>
      <td>83.087886</td>
      <td>83.498795</td>
      <td>83.497041</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.085578</td>
      <td>83.724422</td>
      <td>83.195326</td>
      <td>83.035794</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.264706</td>
      <td>84.010288</td>
      <td>83.836782</td>
      <td>83.644986</td>
    </tr>
  </tbody>
</table>
</div>




```python
# For Reading Scrores (Average) By Grade - Extract the needed columns alone 
#name	gender	grade	school	reading_score	math_score 
reduced_student_readingcolumns = students.loc[:, ['school','grade', 'reading_score']]
#reduced_student_readingcolumns.columns
#reduced_student_readingcolumns.dtypes

#reduced_student_readingcolumns
```


```python
#Get 9th grade Average Reading score by School 
Stu_9thGrade_Reading = reduced_student_readingcolumns[reduced_student_readingcolumns['grade'] == '9th'].groupby('school')['reading_score'].mean()
Stu_9thGrade_ReadingAvg = pd.DataFrame (Stu_9thGrade_Reading)
Stu_9thGrade_ReadingAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_9thGrade_ReadingAvg = Stu_9thGrade_ReadingAvg.rename(columns={"reading_score":"9th"})
#Stu_9thGrade_ReadingAvg.head()
```


```python
#Get 10th grade Average Reading score by School 
Stu_10thGrade_Reading = reduced_student_readingcolumns[reduced_student_readingcolumns['grade'] == '10th'].groupby('school')['reading_score'].mean()
Stu_10thGrade_ReadingAvg = pd.DataFrame (Stu_10thGrade_Reading)

Stu_10thGrade_ReadingAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_10thGrade_ReadingAvg = Stu_10thGrade_ReadingAvg.rename(columns={"reading_score":"10th"})
#Stu_10thGrade_ReadingAvg.head()
```


```python
#Get 11th grade Average Reading score by School 
Stu_11thGrade_Reading = reduced_student_readingcolumns[reduced_student_readingcolumns['grade'] == '11th'].groupby('school')['reading_score'].mean()
Stu_11thGrade_ReadingAvg = pd.DataFrame (Stu_11thGrade_Reading)

Stu_11thGrade_ReadingAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_11thGrade_ReadingAvg = Stu_11thGrade_ReadingAvg.rename(columns={"reading_score":"11th"})
#Stu_11thGrade_ReadingAvg.head()
```


```python
#Get 12th grade Average Reading score by School 
Stu_12thGrade_Reading = reduced_student_readingcolumns[reduced_student_readingcolumns['grade'] == '12th'].groupby('school')['reading_score'].mean()
Stu_12thGrade_ReadingAvg = pd.DataFrame (Stu_12thGrade_Reading)

Stu_12thGrade_ReadingAvg.reset_index(level = 0, inplace = True) # df.reset_index(level=0, inplace=True)
Stu_12thGrade_ReadingAvg = Stu_12thGrade_ReadingAvg.rename(columns={"reading_score":"12th"})
#Stu_12thGrade_ReadingAvg.head()
```


```python
#Merge all the 9th 10h 11th and 12th average Reading grade by school into one table 
merged_9th_10th_AvgReadScore = pd.merge(Stu_9thGrade_ReadingAvg , Stu_10thGrade_ReadingAvg, on="school")

merged_9th_10th_11thAvgReadScore = pd.merge(merged_9th_10th_AvgReadScore , Stu_11thGrade_ReadingAvg, on="school")

merged_9th_10th_11th_12thAvgReadScore = pd.merge(merged_9th_10th_11thAvgReadScore , Stu_12thGrade_ReadingAvg, on="school")

#merged_9th_10th_11th_12thAvgReadScore.head()
```


```python
#Update displays to show in form of table 
display_AvgReadScore_BySchoolGrade = merged_9th_10th_11th_12thAvgReadScore
MathGrade_header ="Reading Scores By Grade"

display_AvgReadScore_BySchoolGrade = display_AvgReadScore_BySchoolGrade.rename(columns={'school':''})

print (color.BOLD + MathGrade_header + color.END)
print('**********************')
display_AvgReadScore_BySchoolGrade
```

    [1mReading Scores By Grade[0m
    **********************





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
      <th></th>
      <th>9th</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>81.303155</td>
      <td>80.907183</td>
      <td>80.945643</td>
      <td>80.912451</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.676136</td>
      <td>84.253219</td>
      <td>83.788382</td>
      <td>84.287958</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>81.198598</td>
      <td>81.408912</td>
      <td>80.640339</td>
      <td>81.384863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>80.632653</td>
      <td>81.262712</td>
      <td>80.403642</td>
      <td>80.662338</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.369193</td>
      <td>83.706897</td>
      <td>84.288089</td>
      <td>84.013699</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>80.866860</td>
      <td>80.660147</td>
      <td>81.396140</td>
      <td>80.857143</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.677165</td>
      <td>83.324561</td>
      <td>83.815534</td>
      <td>84.698795</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>81.290284</td>
      <td>81.512386</td>
      <td>81.417476</td>
      <td>80.305983</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>81.260714</td>
      <td>80.773431</td>
      <td>80.616027</td>
      <td>81.227564</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.807273</td>
      <td>83.612000</td>
      <td>84.335938</td>
      <td>84.591160</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>80.993127</td>
      <td>80.629808</td>
      <td>80.864811</td>
      <td>80.376426</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>84.122642</td>
      <td>83.441964</td>
      <td>84.373786</td>
      <td>82.781671</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.728850</td>
      <td>84.254157</td>
      <td>83.585542</td>
      <td>83.831361</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.939778</td>
      <td>84.021452</td>
      <td>83.764608</td>
      <td>84.317673</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.833333</td>
      <td>83.812757</td>
      <td>84.156322</td>
      <td>84.073171</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Use the mereged school_student Data Table - First, Extract the columns you need  

PerStudentSpending_BySchool.head()

reduced_PerStudentSpending = PerStudentSpending_BySchool.loc[:, ['school','Per Student Budget', 
                                                               'Average Math Score', 'Average Reading Score',
                                                               '% Passing Math', '% Passing Reading', 
                                                               '% Overall Passing Rate']]
#reduced_PerStudentSpending.head()

```


```python
#Parse it to find max per Student Budget and min per Student Budget 
#print(reduced_PerStudentSpending["Per Student Budget"].max())

#print(reduced_PerStudentSpending["Per Student Budget"].min())
```


```python
#Put then in Bins and find average for each data within those bins. TO do this: 

#First - Create bins in which to place values based upon Per Student Spending 
bins = [0,585,615,645,675]

# Second - Create labels for these bins
group_labels = ["< $585","$585-615","$615-645","$645-675"]
```


```python
# Third - Slice the Per Student Budget Data and place it into bins
#pd.cut(reduced_PerStudentSpending["Per Student Budget"], bins, labels=group_labels).head()
```


```python
# Fourth - Place the data series into a new column inside of the DataFrame
reduced_PerStudentSpending["Spending Ranges (Per Student)"] = pd.cut(reduced_PerStudentSpending["Per Student Budget"], bins, labels=group_labels)
    
#reduced_PerStudentSpending
```


```python
#Drop un-needed columns before you group by
reduced_PerStudentSpending.drop(['Per Student Budget'], axis = 1, inplace = True)

# Fifth Step - Create a GroupBy object based upon "Spending Ranges (Per Student)" column
PerStudentSpending_group = reduced_PerStudentSpending.groupby("Spending Ranges (Per Student)")

# Sixth - Find how many rows fall into each bin - Ensure it counts to 15 school which it does 
#print(PerStudentSpending_group["school"].count())

SchoolSpending_Header = "Scores by School Spending"
print (color.BOLD + SchoolSpending_Header + color.END)
print('*************************')

# Finally - Get the average of each column within the GroupBy object - Get Average score on each 
PerStudentSpending_group.mean()
```

    [1mScores by School Spending[0m
    *************************





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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Spending Ranges (Per Student)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt; $585</th>
      <td>83.455399</td>
      <td>83.933814</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.00000</td>
    </tr>
    <tr>
      <th>$585-615</th>
      <td>83.599686</td>
      <td>83.885211</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.00000</td>
    </tr>
    <tr>
      <th>$615-645</th>
      <td>79.079225</td>
      <td>81.891436</td>
      <td>92.636050</td>
      <td>96.264069</td>
      <td>94.45006</td>
    </tr>
    <tr>
      <th>$645-675</th>
      <td>76.997210</td>
      <td>81.027843</td>
      <td>89.041475</td>
      <td>94.520946</td>
      <td>91.78121</td>
    </tr>
  </tbody>
</table>
</div>




```python
# For Scores By School Size 
#First - Extract the columns needed for binning from both the school dataframe
School_Size_Type_Performance.head()

reduced_PerSchoolSize = School_Size_Type_Performance.loc[:, ['school','Total Students']]
#reduced_PerSchoolSize.head()
```


```python
#Extract the columns needed from the aggregated student dataframe 

reduced_PerSchoolScores = PerStudentSpending_BySchool.loc[:, ['school','Average Math Score', 'Average Reading Score',
                                                               '% Passing Math', '% Passing Reading', 
                                                               '% Overall Passing Rate']]
#reduced_PerSchoolScores.head()
```


```python
#Merge to get the combined dataframe that has School Size with performance scores 
merged_SchoolSize_SchoolScores = pd.merge(reduced_PerSchoolSize , reduced_PerSchoolScores, on="school")

#merged_SchoolSize_SchoolScores.head()
```


```python
# Now create the bins to slice the data in the dataframe 

#Parse it to find max Total Students and min Total Students 
#print(merged_SchoolSize_SchoolScores["Total Students"].max())

#print(merged_SchoolSize_SchoolScores["Total Students"].min())
```


```python
#Put then in Bins and find average for each data within those bins. TO do this: 

#First - Create bins in which to place values based upon Total Students
bins = [0,1000,2000,5000]

# Second - Create labels for these bins
group_labels = ["Small (<1000)","Medium (1000-2000)","Large (2000-5000)"]
```


```python
# Third - Slice the Total Students Data and place it into bins
#pd.cut(merged_SchoolSize_SchoolScores["Total Students"], bins, labels=group_labels).head()
```


```python
# Fourth - Place the data series into a new column inside of the DataFrame
merged_SchoolSize_SchoolScores["School Size"] = pd.cut(merged_SchoolSize_SchoolScores["Total Students"], bins, labels=group_labels)
    
#merged_SchoolSize_SchoolScores
```


```python
# Fifth Step - Drop the Total Students column from the list 
merged_SchoolSize_SchoolScores.drop(['Total Students'], axis = 1, inplace = True)

# Sixth Step - Create a GroupBy object based upon "Total Students" column
SchoolSizeScores_group = merged_SchoolSize_SchoolScores.groupby("School Size")

# Seventh Step - Find how many rows fall into each bin - Ensure it counts to 15 school which it does 
#print(SchoolSizeScores_group["school"].count())

SchoolSize_Header = "Scores by School Size"
print (color.BOLD + SchoolSize_Header + color.END)
print('*************************')

# Finally - Get the average of each column within the GroupBy object - Get Average score on each 
SchoolSizeScores_group.mean()
```

    [1mScores by School Size[0m
    *************************





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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small (&lt;1000)</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Medium (1000-2000)</th>
      <td>83.374684</td>
      <td>83.864438</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Large (2000-5000)</th>
      <td>77.746417</td>
      <td>81.344493</td>
      <td>90.367591</td>
      <td>95.143406</td>
      <td>92.755499</td>
    </tr>
  </tbody>
</table>
</div>




```python
# For Scores By School Type 
#First - Extract the columns needed for binning from both the school dataframe
#School_Size_Type_Performance.head()

reduced_PerSchoolType = School_Size_Type_Performance.loc[:, ['school','School Type']]
#reduced_PerSchoolType.head()
```


```python
#Merge to get the combined dataframe that has School Type with performance scores 
merged_SchoolType_SchoolScores = pd.merge(reduced_PerSchoolType , reduced_PerSchoolScores, on="school")

#merged_SchoolType_SchoolScores
```


```python
# First Step - Drop the schools column from the list - Now you have the data needed to get School Type with Scores
merged_SchoolType_SchoolScores.drop(['school'], axis = 1, inplace = True)

```


```python
# Second - Group By School Type and find mean values for each 

AverageScore_BySchoolType = pd.DataFrame(merged_SchoolType_SchoolScores.groupby("School Type").mean())

SchoolType_Header = "Scores by School Type"
print (color.BOLD + SchoolType_Header + color.END)
print('**********************')
AverageScore_BySchoolType
```

    [1mScores by School Type[0m
    **********************





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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.00000</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>88.991533</td>
      <td>94.449607</td>
      <td>91.72057</td>
    </tr>
  </tbody>
</table>
</div>


