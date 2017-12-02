# Py Poll   By: 	Aruna Amaresan 
#			Date: 	Dec 2nd 2017
# Assumption:  
# 				a) User will keep all raw -data to be processed in a folder
#				b) Ensure to keep all input files to be processed in raw_data folder under the nameformat as 
#					election_data_1.csv, election_data_2.csv and so forth
#				c) An output folder needs to be created under the same tree level as raw_data folder.
#				c) CSV file needs have the format of 3 entries on every row separated by "," and have column headers as 
#					VoterID, County and Candidate
#					 specified. We expect the header to be present in the first row. 
#				d) The raw_data folder and output folder needs to exist and file count needs to be less than or equal to 
#					number of files actually present for processing   
#			
# Description: 
#				Input: The program will request for the number of such files to be processed and will 
#						review those files one at a time
# 
#				Output: It will process each file and write the output data into console and a file  with file name format 
#						election_summary_X where X is the file number. 
#
#				Example: If user requested that 2 files be process, it will look for, 
#					a) election_data_1.csv . Then read and process it and then write output in output folder with file name election_summary_1.csv
#					b) election_data_2.csv . Then read and process it and then write output in output folder with file name election_summary_2.csv
#
########################################################################################	


#Import dependencies 
import os
import csv
import numpy as np

# Read files from their input election_data_1.csv
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
	
	# Create file folder name for reading election data 
	voteCSV = os.path.join('raw_data', 'election_data_' + str(fileNo+1) + '.csv')

	# Create new summary TEXT file
	summaryVoteTXT = os.path.join( 'output', 'election_summary_' + str(fileNo+1) + '.txt')

	# Set empty list variables
	Candidates = []
	#monthly_revenue = []
	#totalRevenue =float(0)
	#max_rev = float(0)
	# max_rev_month = ""
	# min_rev = float(0)
	# min_rev_month =""

	summaryOutput = 'Election Results \n-------------------------------------------------\n'
	concat_totalVote_output = 'Total Votes: {0} \n-------------------------------------------------\n'
	#Total Revenue: $ {1:.2f} \nAverage Revenue Change: $ {2:.2f} \n'
	concat_candidate_info = '{0}:	{1:.1f}% 	({2})\n'
	concat_winning_candidate = '-------------------------------------------------\nWinner:	{0}\n-------------------------------------------------\n'

	# Open current bank CSV file - TODO: Need to handle error if file open gives an error as the file cant be found 
	with open(voteCSV, 'r') as csvFile:
		csvReader = csv.reader(csvFile, delimiter=',')
		# Skip headers
		next(csvReader, None)

		for row in csvReader: 
			#Append data from the row
			#print(str(row[0]))
			#print(str(row[1]))
			Candidates.append(row[2])
			#monthly_revenue.append(float(row[1]))
			#totalRevenue = totalRevenue + float(row[1])

	# Write output data into file 
	voteSummaryFile = open(summaryVoteTXT,'w')

	voteSummaryFile.write( summaryOutput + concat_totalVote_output.format(len(Candidates)) ) 

	print (summaryOutput + concat_totalVote_output.format(len(Candidates)) )
	# Read the list into ndarray to get unique counts 
	candidate_array = np.array(Candidates)
	unique_candidates, candidate_count = np.unique(candidate_array, return_counts=True)

	#print(np.asarray((unique_candidates, candidate_count)).T)
	unique_candidates_array = np.asarray((unique_candidates, candidate_count)).T
	winning_candidate = ""
	winning_vote_count = 0

	for candidate in unique_candidates_array:
		#print(str(candidate[0]) + str(candidate[1]))
		votecount = float(candidate[1])
		if (winning_vote_count <= votecount):
			winning_vote_count = votecount
			winning_candidate = str(candidate[0])

		candidate_count_percentage = (float(votecount / len(Candidates)) * 100)
		#print("Candidate percentage: " + str(candidate_count_percentage))
		print(concat_candidate_info.format(candidate[0], candidate_count_percentage, candidate[1]))
		voteSummaryFile.write( concat_candidate_info.format(candidate[0], candidate_count_percentage, candidate[1]) )


	print(concat_winning_candidate.format(winning_candidate))
	voteSummaryFile.write( concat_winning_candidate.format(winning_candidate) )
	
	voteSummaryFile.close()
	