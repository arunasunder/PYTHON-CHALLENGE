# 
# Program: 		Python Bank - 	By: 	Aruna Amaresan 
#								Date: 	Dec 1st 2017
# Assumption:  
# 				a) User will keep all raw -data to be processed in a folder
#				b) Ensure to keep all input files to be processed in raw_data folder under the nameformat as 
#					budget_data_1.csv, budget_data_2.csv and so forth
#				c) CSV file needs have the format of 2 entries on every row separated by "," and have Date, Revenue amount
#					 specified. We expect the header to be present in the first row. 
#				d) The raw_data folder and output folder needs to exist and file count needs to be less than or equal to 
#					number of files actually present for processing   
#			
# Description: 
#				Input: The program will request for the number of such files to be processed and will 
#						review those files one at a time
# 
#				Output: It will process each file and write the output data into a file  with file name format budget_summary_X 
#						where X is the file number. 
#
#				Example: If user requested that 2 files be process, it will look for, 
#					a) budget_data_1.csv . Then read and process it and then write output in output folder with file name budget_summary_1.csv
#					b) budget_data_2.csv . Then read and process it and then write output in output folder with file name budget_summary_2.csv
#
########################################################################################					

#Import Dependencies 
import os
import csv


#Get a Valid number of file count as Input from user 
run = True

while run == True:
	
	file_count = int(input("Enter number of Bank Data files to process? "))
	
	if (file_count <= 0):
		print("You entered " + str(file_count) + ". File count needs to be greater than 0. Please re-enter a number greater than 0.")
	else:
		run = False

# Read the Bank Data csv file one at a time and process it 
for fileNo in range(file_count):
	#print(fileNo)
	#print('I am starting read of CSV file')

	# Grab bank data CSV
	bankCSV = os.path.join('raw_data', 'budget_data_' + str(fileNo+1) + '.csv')

	#print(bankCSV)

	# Create new summary TEXT file
	summaryBankTXT = os.path.join( 'output', 'budget_summary_' + str(fileNo+1) + '.txt')

	#print(summaryBankTXT)

	# Set empty list variables
	month_of_revenue = []
	monthly_revenue = []
	totalRevenue =float(0)
	max_rev = float(0)
	max_rev_month = ""
	min_rev = float(0)
	min_rev_month =""

	summaryOutput = 'Financial Analysis \n-------------------------------------------------\n'
	concat_output = 'Total Months: {0} \nTotal Revenue: $ {1:.2f} \nAverage Revenue Change: $ {2:.2f} \n'
	concat_max_min = 'Greatest Increase in Revenue: {0} ($ {1:.2f}) \nGreatest Decrease in Revenue: {2} ($ {3:.2f})\n'

	# Open current bank CSV file - TODO: Need to handle error if file open gives an error as the file cant be found 
	with open(bankCSV, 'r') as csvFile:
		csvReader = csv.reader(csvFile, delimiter=',')
		# Skip headers
		next(csvReader, None)

		for row in csvReader: 
			#Append data from the row
			#print(str(row[0]))
			#print(str(row[1]))
			month_of_revenue.append(row[0])
			monthly_revenue.append(float(row[1]))
			totalRevenue = totalRevenue + float(row[1])


	#Zip lists together
	tupleBankCSV = zip(month_of_revenue, monthly_revenue)
	#print (tupleBankCSV)

	averageRevenue = totalRevenue / (float(len(monthly_revenue)))
	#print ('Average Revenue Change: $' + str(averageRevenue) )

	# Get the max min pair (month and revenue)
	for month, rev in tupleBankCSV:
		if (rev == max(monthly_revenue) ):
			max_rev = rev
			max_rev_month = month
		if (rev == min(monthly_revenue) ):
			min_rev = rev
			min_rev_month = month

	print (summaryOutput + concat_output.format(len(month_of_revenue), totalRevenue, averageRevenue) + 
		concat_max_min.format(max_rev_month, max_rev, min_rev_month, min_rev))

	# Write output data into file 
	summaryFile = open(summaryBankTXT,'w')

	summaryFile.write(summaryOutput + concat_output.format(len(month_of_revenue), totalRevenue, averageRevenue) + 
		concat_max_min.format(max_rev_month, max_rev, min_rev_month, min_rev))

	summaryFile.close()


