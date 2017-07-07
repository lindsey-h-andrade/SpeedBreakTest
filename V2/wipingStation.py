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

cornerStarts = {
	0: {'X': 0, 'Y': 0}, 
	1: {'X': 0, 'Y': YMAX},
	2: {'X': XMAX, 'Y': YMAX}, 
	# 3: {'X': XMAX, 'Y': 0}, 
	3: {'X': XMAX/2, 'Y': YMAX/2} # The center of the print bed
}

def main():
	# Set up output file
	resultFile = open('WipingStationSpeedResults.txt', 'a')
	resultFile.write("%s Test Run Started \n" % (datetime.now()))

	testDescription = input("Test Description: ")
	resultFile.write("%s, %s \n" %(datetime.now(), testDescription))

	# Define wiping speed ranges
	speeds = range(9000, 1000, -1000)

	numOfCorners = len(cornerStarts.keys())
	numOfSpeeds = len(speeds)

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
		for j in range(numOfSpeeds):
			stringForCopy = stringForCopy + createGcodeCopy(i, speeds[j])
			pyperclip.copy(stringForCopy) # Stays at 1 Corner, goes through all speeds

			print('---------------------------')
			print("Corner %d, F%d" %(i, speeds[j]))
			print("Paste new commands.")

			
			BREAK = input("Did filament break? [y/n] ")

			if BREAK == 'y': 
				print('Filament broken. Use M113 to stop current movement.')
				time.sleep(4)

				brokenMat = ""

				MATERIAL = input("Which filament broke? [1 - Metal, 2 - Ceramic] ")
				if MATERIAL == "1": 
					brokenMat = "Metal"
				else: 
					brokenMat = "Ceramic"

				stringForCopy = ""
				
				resultFile.write("%s broke at: Corner %d, Speed %d \n" % (brokenMat, i, speeds[j]))
				print('Results Recorded')

				CONTINUE = input("Continue testing more sizes at this corner? [y/n] ")
				if CONTINUE == "n": 
					break


			elif BREAK == 'n': 
				# Ask if want to continue testing lower speeds
				CONTINUE = input('Continue testing lower speeds? [y/n] ')
				if CONTINUE == "n": 
					break
				# Clear string and move onto the next speed group
				stringForCopy = ""

		stringForCopy = ""


def createGcodeCopy(corner, speed): 
	returnString = ""

	Xstart = cornerStarts[corner]['X']
	Ystart = cornerStarts[corner]['Y']

	returnString = returnString + "G92 E0\n"
	returnString = returnString + "G0 X%d Y%d F%d \n" %(Xstart, Ystart, speed)
	returnString = returnString + "G0 E11 \n"
	returnString = returnString + "G0 X300 Y5 \nG0 Y10 \nG0 X330 \nG0 Y15 \nG0 X300 \nG0 Y20 \nG0 X330 \nG0 Y25 \nG0 X300 \nG0 Y30 \nG0 X330 \nG0 Y35 \nG0 X300 \nG0 X280 Y10 \nG92 E0 \n"

	return returnString

# Raw wiping station code
	# G0 X300 Y5 F2000
	# G0 Y10
	# G0 X330
	# G0 Y15
	# G0 X300
	# G0 Y20
	# G0 X330
	# G0 Y25
	# G0 X300
	# G0 Y30
	# G0 X330
	# G0 Y35
	# G0 X300
	# G0 X280 Y10
	# G92 E0
	# G1 F500
	# G0 F1200

if __name__ == "__main__": 
	print('******************************************************')
	# createGcodeCopy(4, 2000, 10)
	# createGcodeCopy(1, 2000, 20)
	main()
	closeProgram = input("")