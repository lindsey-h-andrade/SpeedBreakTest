from gcodeInit import addInit
from math import sqrt
import pyperclip
import time
from conditions import conditions
from datetime import datetime

def main():

	# Run number counter
	count = 1
	numberOfTests = 2

	# Open results text file
	resultFile = open('SpeedResults.txt', 'a')
	resultFile.write("%s Test Run Started \n" % (datetime.now()))

	testDescription = input("Test Description: ")
	if testDescription != "": 
		resultFile.write("%s, %s \n" %(datetime.now(), testDescription))


	# Start printer sequence
	printerInitialConditions = ""
	master = open('gcodeInitMaster.txt', 'r').readlines()
	printerInitialConditions = "".join(master)

	pyperclip.copy(printerInitialConditions)
	print('Paste printer start-up commands')
	time.sleep(1)

	uinput1 = input('Done heating T0 to 200 and bed dropped down? [y/n] ')
	doneSetup(uinput1)

	# Only gets to this point if doneSetup input is 'y'

	for j in conditions: 
		# Pull from conditions file
		mini = conditions[j]['mini']
		maxi = conditions[j]['maxi']
		headspeed = conditions[j]['headspeed']
		stepLength = conditions[j]['stepLength']
		# -- end pull from conditions file

		stepPosition = mini[1] - stepLength

		w, h = 2, int((maxi[1]-mini[1])/stepLength)

		positions = [[None for x in range(w)] for y in range(h)]

		for i in range(h):
			# print(i+1)
			if (i) % 2 == 0:
				positions[i][0] = maxi[0]
			else: 
				positions[i][0] = mini[0]

			stepPosition = stepPosition + stepLength

			positions[i][1] = stepPosition

		# calculate E values for each move
		epmm = 0.03379586445901975 # extrusion per mm of movement
		E = [0 for x in range(0, h+1)]

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

		arrayForCopy = []

		for i in range(0,h): 
			if i == 0: 
				string = "G92 E0 \n G0 X%f Y%f F%f \n" % (positions[i][0], positions[i][1], headspeed)
			else: 
				string = "G92 E0 \n G0 X%f Y%f E%f \n" % (positions[i][0], positions[i][1], E[i])
				# string = "G92 E0 \n G0 X%f Y%f E%f \n" % (positions[i][0], positions[i][1], 0) # no extrude
			
			arrayForCopy.append(string)

		stringForCopy = "".join(arrayForCopy)

		pyperclip.copy(stringForCopy)

		print('Test %d ready for paste into Eiger' % (j))
		time.sleep(1)

		uinput2	= input("Did filament break? [y/n] ")
		print("----------")

		# Write conditions and pass/fail into results text file
		resultFile.write("%s, " %(str(datetime.now())))
		resultFile.write('Test number %d, Range from: (%f, %f) to: (%f, %f), Headspeed: %f, Y step: %f, ' %(j, mini[0], mini[1], maxi[0], maxi[1], headspeed, stepLength))
		if uinput2 == "y": 
			resultFile.write('Fail \n')
			print("!!!!!!!!!!!!!")
			uinput3 = input('Continue with testing? [y/n] ')
			print("----------")
			if uinput3 == 'n':
				break
		else:
			resultFile.write('Pass \n')
			

	# Testing Ended
	print("Testing Ended")

	resultFile.write("%s Test Run Ended \n" % (datetime.now()))
	resultFile.write("--------------------------------------- \n")

	resultFile.close()

def doneSetup(uinput1): 
	if uinput1 == 'y': 
		print('Printer ready for extrusion.')
		time.sleep(1)
		
	elif uinput1 == 'n': 
		print('Wait...')
		time.sleep(5)
		uinput1 = input('Done heating T0? [y/n] ')
		doneSetup(uinput1)
	else: 
		uinput1 = input('Done heating T0? [y/n] ')
		doneSetup(uinput1)



if __name__ == "__main__": 
	
	main()
		
	