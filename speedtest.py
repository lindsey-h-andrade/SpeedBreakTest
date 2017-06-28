from gcodeInit import addInit
from math import sqrt

def main(): 
	gcodeOutput = 'gru.gcode'
	addInit(gcodeOutput)

	f = open(gcodeOutput, "a+")

	# drop the Z height down to 100
	f.write('G0 Z100 F1200 \n')

	# init x and y minimum and maximum positions
	mini = [0, 0]
	maxi = [200, 100]

	# define movement speed of head
	headspeed = 2000

	# init position array
	# position[a][b] where [a] is the point and [b] is x (0) or y (1) 
	w, h = 2, 24 # h needs to be a multiple of 4 (right now) will need to be dependent on Max Y value at some point
	positions = [[None for x in range(w)] for y in range(h)]
	
	stepLength = 5
	stepPosition = mini[1] - stepLength

	for i in range(h):
		# print(i+1)
		if (i) % 2 == 0:
			positions[i][0] = maxi[0]
		else: 
			positions[i][0] = mini[0]

		stepPosition = stepPosition + stepLength

		positions[i][1] = stepPosition





			# # set the x positions which just go back and forth between max and min X
			# positions[i][0] = maxi[0]
			# positions[i-1][0] = mini[0]
			# positions[i-2][0] = mini[0]
			# positions[i-3][0] = maxi[0]

			# # set the y positions
			# stepPosition = stepPosition + (2*stepLength)

			# positions[i][1] = stepPosition
			# positions[i-1][1] = stepPosition
			# positions[i-2][1] = stepPosition - stepLength
			# positions[i-3][1] = stepPosition - stepLength

	# print(positions)



	# calculate E values for each move
	epmm = 0.03379586445901975 # extrusion per mm of movement
	E = [0 for x in range(0, h+1)]
	# print(E[h-1])

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

	for i in range(0,h): 
		if i == 0: 
			string = "G0 X%f Y%f F%f \n" % (positions[i][0], positions[i][1], headspeed)
		else: 
			string = "G0 X%f Y%f E%f \n" % (positions[i][0], positions[i][1], E[i])
		
		f.write(string)


		



if __name__ == '__main__': 
	main()