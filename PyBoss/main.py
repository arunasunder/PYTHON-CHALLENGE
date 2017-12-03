# PyBoss   -  By: 	Aruna Amaresan 
#			Date: 	Dec 2nd 2017
# Assumption:  
# 				a) User will keep all raw-data to be processed in a folder
#				b) Ensure to keep all input files to be processed in raw_data folder under the nameformat as 
#					employee_data1.csv, employee_data2.csv and so forth
#				c) An output folder needs to be created under the same tree level as raw_data folder.
#				c) CSV file needs to have a format with 3 entries on every row separated by "," and have column headers as 
#					Emp ID, Name, DOB, SSN and State. We expect the header to be present in the first row. 
#				d) The raw_data folder and output folder needs to exist and file count needs to be less than or equal to 
#					number of files actually present for processing   
#			
# Description: 
#				Input: The program will request for the number of such files to be processed and will 
#						review those files one at a time
# 
#				Output: It will process each file and write the output data into a file  with file name format 
#						revised_employee_data_X where X is the file number. 
#	
#
#				Example: If user requested that 2 files be process, it will look for, 
#					a) employee_data1.csv . Then read and process it and then write output in output folder with file name revised_employee_data_1.csv
#					b) employee_data2.csv . Then read and process it and then write output in output folder with file name revised_employee_data_2.csv
#
########################################################################################


# Initialize the US States dictionary to look up and get the key value pair to replace
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

#Import dependencies 
import os
import csv
import numpy as np

# Read files from their input election_data_1.csv
#Get a Valid number of file count as Input from user 
run = True

while run == True:
	
	file_count = int(input("Enter number of Employee Data files you need to process? "))
	
	if (file_count <= 0):
		print("You entered " + str(file_count) + ". File count needs to be greater than 0. Please re-enter a number greater than 0.")
	else:
		run = False

# Read the Employee Data csv file one at a time and process it 
for fileNo in range(file_count):
	
	# Create file folder name for reading election data 
	empDataCSV = os.path.join('raw_data', 'employee_data' + str(fileNo+1) + '.csv')

	# Create new revised Employee Data file
	revised_empDataCSV = os.path.join( 'output', 'revised_employee_data_' + str(fileNo+1) + '.csv')

	# Set empty list variables
	EmpID = []
	First_Name = []
	Last_Name = []
	DOB = []
	SSN = []
	State = []
	revised_DOB = '{0:02d}/{1:02d}/{2:04d}'
	revised_SSN = '***-**-{0:04d}'

	# Open current employee Data CSV file - TODO: Need to handle error if file open gives an error as the file cant be found 
	with open(empDataCSV, 'r') as csvFile:
		csvReader = csv.reader(csvFile, delimiter=',')
		# Skip headers
		next(csvReader, None)

		for row in csvReader:

			#Read Employee ID 
			EmpID.append(row[0])
			#print(str(row[0]))

			#Read the Employee Name 
			#print(str(row[1]))

			# Parse to get First Name and Last Name 
			# example 1: 	Name: Sandra Anderson
			# 			First Name = Sandra		Last Name = Anderson
			# example 2: 	Name = Lilly Rose Potter
			#			First Name = Lilly		Last Name = Rose Potter 
			Split_Names = row[1].split(" ")

			#Append First Name 
			First_Name.append(Split_Names[0]) 
			array_length = len(Split_Names)
			#print ("First Name: " + Split_Names[0])
			#print ("Length of Split Name Array: " + str(len(Split_Names)))

			#Append Last name 
			if (array_length > 2):
				#If there is a middle name - assume only 2 more parts to the name, Middle & Last and append to Last_Name
				middleLast_name = Split_Names[1] + " " + Split_Names[2]
				#print("Concat and Print Name Test: " + str(middleLast_name))
				Last_Name.append(middleLast_name)
			else:
				Last_Name.append(Split_Names[1])

			#print ("Last Name: " + Split_Names[1])

			#Get DOB and rewrite in updated format
			#print(str(row[2]))

			#Reformat DOB from DD-MM-YYYY to MM/DD/YYYY
			Split_DOB = row[2].split("-")
			year = int(Split_DOB[0])
			month = int(Split_DOB[1])
			date = int(Split_DOB[2])

			#print( revised_DOB.format(month, date, year) )

			#Append revised DOB
			DOB.append(revised_DOB.format(month, date, year))

			#Get SSN info 
			#print(str(row[3]))

			# Parse SSN to hide first 5 characetrs, then re-write and store
			Split_SSN = row[3].split("-")

			#If SSN last 4 digits present then write it, otherwise just put 0s
			SSN_last_four_digits = 0000

			if (len(Split_SSN) > 2):
				SSN_last_four_digits = int(Split_SSN[2])

			#print( revised_SSN.format(SSN_last_four_digits) )

			#Append the revised SSN
			SSN.append(revised_SSN.format(SSN_last_four_digits))

			#Get State Name
			ReadState = str(row[4])
			#print( ReadState )

			# Parse, re-write and store as 2 letter abbreviated state code codes 
			#if you cant find the State code write NaN for missing state coded
			stateCode = us_state_abbrev.get(ReadState, 'NaN')
			
			#Append the STATE code 
			State.append(stateCode)
			#print ("State Code: " + str(stateCode))


	#Zip the list to forma tuple ready to be written into CSV file 
	cleaned_emp_data = zip( EmpID, First_Name, Last_Name, DOB, SSN, State)


	#Write into CSV file 
	with open(revised_empDataCSV, 'w', newline="") as csvFile:

		csvWriter = csv.writer(csvFile, delimiter=',')

		# Write Headers into file
		csvWriter.writerow([ "EmpID", "First Name", "Last Name", "DOB", "SSN", "State"])

		# Write the zipped lists to a csv
		csvWriter.writerows( cleaned_emp_data )

print ("Processing complete! Check your output folder for processed CSV files.")
print ("Have a nice day!")

