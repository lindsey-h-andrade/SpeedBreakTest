from math import sqrt # To calculate the extrusion amount per move
import pyperclip # To copy strings to the clipboard
import time # To use sleep and delay functions
from datetime import datetime # To get the current date and time of a test run

# Set max X and Y dimensions 
XMAX = 330
YMAX = 250

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
	resultFile = open('SpeedResults.txt', 'a')
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
				if MATERIAL == 1: 
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

	if Xstart + size < XMAX and Xstart - size < 0: 
		# print('Right edge')
		xGoto = Xstart + size

		if Ystart + size > YMAX: 
			# print('Think it\'s at Corner 1. Actually at Corner %d' %(corner))
			yGoto = Ystart - size  

		elif Ystart - size < 0: 
			# print('Thick it\'s at Corner 0. Actually at Corner %d' %(corner))
			yGoto = Ystart + size

	elif Xstart + size > XMAX and Xstart - size > 0: 
		# print('Left edge')
		xGoto = Xstart - size

		if Ystart + size > YMAX: 
			# print('Think it\'s at Corner 2. Actually at Corner %d' %(corner))
			yGoto = Ystart - size

		elif Ystart - size < 0: 
			# print('Thick it\'s at Corner 3. Actually at Corner %d' %(corner))
			yGoto = Ystart + size

	elif Xstart + size < XMAX and Xstart - size  > 0: 
		# print('Middle of X')
		if Ystart + size < YMAX and Ystart - size > 0: 
			xGoto = Xstart - size/2
			yGoto = Ystart - size/2

			# print('Thick it\'s at Corner 4. Actually at Corner %d' %(corner))

	# Init the positions array
	w, h = 2, size
	positions = [[None for x in range(w)] for y in range(h)]

	# Set initial X and Y positions
	if xGoto < Xstart: 
		positions[0][0] = xGoto
	else: 
		positions[0][0] = Xstart

	if yGoto < Ystart: 
		positions[0][1] = yGoto
	else: 
		positions[0][1] = Ystart

	# Populate the positions array
	for i in range(1, size): 
		if positions[i - 1][0] == xGoto: 
			positions[i][0] = Xstart
		else: 
			positions[i][0] = xGoto

		positions[i][1] = positions[i-1][1] + 1

	# print(positions) # looks good

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
	for i in range(size): 
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