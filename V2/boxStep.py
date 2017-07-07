from math import sqrt # To calculate the extrusion amount per move
import pyperclip # To copy strings to the clipboard
import time # To use sleep and delay functions
from datetime import datetime # To get the current date and time of a test run

# Set max X and Y dimensions 
XMAX = 330 # Same for both Mark X and Mark 2 chassis

printerModel = input("Testing on which printer chassis? [1 - Mark 2, 2 - Mark X] ")

if printerModel == "1": 
	YMAX = 130 # Mark 2 size
elif printerModel == "2": 
	YMAX = 250 # Mark X size

# Define the X and Y starting potitions of the corners 	
cornerStarts = {
	0: {'X': 0, 'Y': 0}, 
	1: {'X': 0, 'Y': YMAX},
	2: {'X': XMAX, 'Y': YMAX}, 
	3: {'X': XMAX, 'Y': 0}, 
	4: {'X': XMAX/2, 'Y': YMAX/2} # The center of the print bed
}

def main():
	# Set up output file
	resultFile = open('BoxStepSpeedResults.txt', 'a')
	resultFile.write("%s Test Run Started \n" % (datetime.now()))

	testDescription = input("Test Description: ")
	resultFile.write("%s, %s \n" %(datetime.now(), testDescription))

	# Define speed ranges
	speeds = range(6000, 1000, -1000)

	# Set size range
	sizes = range(10, 110, 10)

	numOfCorners = len(cornerStarts.keys())
	numOfSpeeds = len(speeds)
	numOfSizes = len(sizes)

	# Initialize the string for user to copy into Eiger terminal
	stringForCopy = ""


	# Initialize Printer
	printerInitialConditions = ""
	master = open('gcodeInitMaster.txt', 'r').readlines()
	printerInitialConditions = "".join(master)

	pyperclip.copy(printerInitialConditions)
	print('Paste printer start-up commands')
	time.sleep(1)

	uinput1 = input('Done heating T0 to 200 and bed dropped down? [y/n] ')

	for i in range(numOfCorners):
		print('--------------------------Corner Change--------------------------')
		
		for j in range(numOfSpeeds):
			print('-------------Speed Change-------------')

			for k in range(numOfSizes): 
				stringForCopy = stringForCopy + createGcodeCopy(i, speeds[j], sizes[k])
				# print(speeds[j])

				print('Corner %d, F%d, %d' %(i, speeds[j], sizes[k]))



			pyperclip.copy(stringForCopy) # Stays at 1 Corner, goes through all speed and sizes
			BREAK = input("Did filament break? [y/n] ")

			if BREAK == 'y': 
				print('Filament broken. Use M113 to stop current movement.')
				time.sleep(5)

				brokenMat = ""

				MATERIAL = input("Which filament broke? [1 - Metal, 2 - Ceramic] ")
				if MATERIAL == "1": 
					brokenMat = "Metal"
				else: 
					brokenMat = "Ceramic"

				stringForCopy = ""  

				# Ask if break after each speed, go through all sizes. Start at fastest speed if possible.
				for l in range(numOfSizes): 
					stringForCopy = stringForCopy + createGcodeCopy(i, speeds[j], sizes[l])
					pyperclip.copy(stringForCopy)

					print("Corner %d, F%d, %d" %(i, speeds[j], sizes[l]))
					print("Paste new commands.")
					BREAK = input("Did filament break? [y/n] ")

					if BREAK == 'y': 
						resultFile.write("%s broke at: Corner %d, Speed %d, Size %d \n" % (brokenMat, i, speeds[j], sizes [l]))
						CONTINUE = input("Continue testing more sizes at this speed? [y/n] ")
						if CONTINUE == "n": 
							break
					elif BREAK == 'n':
						if l == numOfSizes - 1: 
							resultFile.write("%s broke at: Corner %d, Speed %d, Unknown Size" %(brokenMat, i, speeds[j]))
						
						stringForCopy = ""

			elif BREAK == 'n': 
				# Ask if want to continue testing lower speeds
				CONTINUE = input('Continue testing lower speeds? [y/n] ')
				if CONTINUE == "n": 
					break
				# Clear string and move onto the next speed group
				stringForCopy = ""

		stringForCopy = ""	
			
		

	

def createGcodeCopy(corner, speed, size):
	Xstart = cornerStarts[corner]['X']
	Ystart = cornerStarts[corner]['Y']


	# Init the positions array
	w, h = 2, 4
	positions = [[None for x in range(w)] for y in range(h)]

	if corner == 0: 
		positions[0][0] = Xstart
		positions[0][1] = Ystart

		positions[1][0] = Xstart
		positions[1][1] = Ystart + size

		positions[2][0] = Xstart + size
		positions[2][1] = Ystart + size

		positions[3][0] = Xstart + size
		positions[3][1] = Ystart
	elif corner == 1: 
		positions[0][0] = Xstart
		positions[0][1] = Ystart - size

		positions[1][0] = Xstart
		positions[1][1] = Ystart

		positions[2][0] = Xstart + size
		positions[2][1] = Ystart

		positions[3][0] = Xstart + size
		positions[3][1] = Ystart - size
	elif corner == 2: 
		positions[0][0] = Xstart - size
		positions[0][1] = Ystart - size

		positions[1][0] = Xstart - size
		positions[1][1] = Ystart

		positions[2][0] = Xstart 
		positions[2][1] = Ystart

		positions[3][0] = Xstart
		positions[3][1] = Ystart - size
	elif corner == 3: 
		positions[0][0] = Xstart - size
		positions[0][1] = Ystart

		positions[1][0] = Xstart - size
		positions[1][1] = Ystart + size

		positions[2][0] = Xstart 
		positions[2][1] = Ystart + size

		positions[3][0] = Xstart
		positions[3][1] = Ystart 
	elif corner == 4: 
		positions[0][0] = Xstart - size/2
		positions[0][1] = Ystart - size/2

		positions[1][0] = Xstart - size/2
		positions[1][1] = Ystart + size/2

		positions[2][0] = Xstart + size/2
		positions[2][1] = Ystart + size

		positions[3][0] = Xstart + size/2
		positions[3][1] = Ystart - size/2


	# calculate E values for each move
	epmm = 0.03379586445901975 # extrusion per mm of movement
	E = [0 for x in range(0, h)]

	for i in range(1, h): 
		pos1 = positions[i]
		pos2 = positions[i - 1]

		x1 = pos1[0]
		y1 = pos1[1] 
		x2 = pos2[0]
		y2 = pos2[1]

		# calculate the distance between the origin of a move and the end of a move
		dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)

		E[i] = dist * epmm

	returnString = ""
	for i in range(h): 
		returnString = returnString + "G92 E0\n"
		if E[i] == 0: 
			returnString = returnString + "G0 X%f Y%f F%f \n" % (positions[i][0], positions[i][1], speed)
		else: 
			returnString = returnString + "G0 X%f Y%f E%f \n" % (positions[i][0], positions[i][1], E[i])
			# returnString = returnString + "G0 X%f Y%f \n" % (positions[i][0], positions[i][1]) # No extrusion 

	# pyperclip.copy(returnString)
	return returnString

if __name__ == "__main__": 
	print('******************************************************')
	# createGcodeCopy(4, 2000, 10)
	# createGcodeCopy(1, 2000, 20)
	main()
	closeProgram = input("")