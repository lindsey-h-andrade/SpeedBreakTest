def main(): 
	print('Running gcodeInit')
	gcodeResult = open("guru99.gcode", "w+")
	gcodeResult.write('#first')	

def addInit(filename): 

	with open('gcodeInitMaster.txt', 'r') as master: 
		with open(filename, "w+") as gcodeResult: 
			for line in master:
				gcodeResult.write(line) 

	gcodeResult.close()	

if __name__ == '__main__': 
	main()


# ;R:1
# G21
# G90
# M400
# G92 E0
# T0 F2000
# M92 E186
# ;F:0
# G28 X0 Y0
# G92 
# M201 X1400 Y1400
# M203 X208.33333333333334 Y208.33333333333334
# M107 P0 
# M106 P1 S255
# M104 T0 S200
# M109 T1 S130
# M109 T0 S200
# M106 P2 S255
# G28 Z0
# G92 