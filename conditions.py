# 1 - 5:  50mm square at back right corner, stepping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000.
# 6 - 10:  50mm square at front left corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000.
# 11 - 15:  50mm square at front right corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000. 
# 16 - 20:  50 mm square at back left corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000. 
# 21 - 25: 50 mm square at center of build plate, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000. 
# 26 - 30: Full build plate coverage, stepping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000.
# 31 - 35: Full build plate coverage, stepping up by 20mm in the Y direction. Sweeping head speed from 2000 to 6000.

maxX = 330
maxY = 250

minSpeed = 2000
maxSpeed = 6000

speedStep = (maxSpeed-minSpeed)/4
a = minSpeed
b = minSpeed + speedStep
c = minSpeed + speedStep*2
d = minSpeed + speedStep*3
e = minSpeed + speedStep*4

conditions = {
			# # 50mm square at back right corner, stepping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000.
			# 1: {"mini":[0, 0], 
			# 	"maxi": [50, 50], 
			# 	"headspeed" : a, 
			# 	"stepLength": 5}, 
			# 2: {"mini":[0, 0], 
			# 	"maxi": [50, 50], 
			# 	"headspeed" : b, 
			# 	"stepLength": 5}, 
			# 3: {"mini":[0, 0], 
			# 	"maxi": [50, 50], 
			# 	"headspeed" : c, 
			# 	"stepLength": 5}, 
			# 4: {"mini":[0, 0], 
			# 	"maxi": [50, 50], 
			# 	"headspeed" : d, 
			# 	"stepLength": 5}, 
			# 5: {"mini":[0, 0], 
			# 	"maxi": [50, 50], 
			# 	"headspeed" : e, 
			# 	"stepLength": 5}, 
			# 50mm square at front left corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000.
			6: {"mini":[maxX - 50, maxY - 50], 
				"maxi": [maxX, maxY], 
				"headspeed" : a, 
				"stepLength": 5}, 
			7: {"mini":[maxX - 50, maxY - 50], 
				"maxi": [maxX, maxY], 
				"headspeed" : b, 
				"stepLength": 5}, 
			8: {"mini":[maxX - 50, maxY - 50], 
				"maxi": [maxX, maxY], 
				"headspeed" : c, 
				"stepLength": 5}, 
			9: {"mini":[maxX - 50, maxY - 50], 
				"maxi": [maxX, maxY], 
				"headspeed" : d, 
				"stepLength": 5}, 
			10: {"mini":[maxX - 50, maxY - 50], 
				"maxi": [maxX, maxY], 
				"headspeed" : e, 
				"stepLength": 5}, 
			# # 50mm square at front right corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000. 
			# 11: {"mini":[0, maxY-50], 
			# 	"maxi": [50, maxY], 
			# 	"headspeed" : a, 
			# 	"stepLength": 5}, 
			# 12: {"mini":[0, maxY-50], 
			# 	"maxi": [50, maxY], 
			# 	"headspeed" : b, 
			# 	"stepLength": 5}, 
			# 13: {"mini":[0, maxY-50], 
			# 	"maxi": [50, maxY], 
			# 	"headspeed" : c, 
			# 	"stepLength": 5}, 
			# 14: {"mini":[0, maxY-50], 
			# 	"maxi": [50, maxY], 
			# 	"headspeed" : d, 
			# 	"stepLength": 5}, 
			# 15: {"mini":[0, maxY-50], 
			# 	"maxi": [50, maxY], 
			# 	"headspeed" : e, 
			# 	"stepLength": 5}, 
			# # 50 mm square at back left corner, steeping by 10mm in the Y direction. Sweeping head speed from 2000 to 6000. 
			# 16: {"mini":[maxX-50, 0], 
			# 	"maxi": [maxX, 50], 
			# 	"headspeed" : a, 
			# 	"stepLength": 5}, 
			# 17: {"mini":[maxX-50, 0], 
			# 	"maxi": [maxX, 50],
			# 	"headspeed" : b, 
			# 	"stepLength": 5}, 
			# 18: {"mini":[maxX-50, 0], 
			# 	"maxi": [maxX, 50], 
			# 	"headspeed" : c, 
			# 	"stepLength": 5}, 
			# 19: {"mini":[maxX-50, 0], 
			# 	"maxi": [maxX, 50], 
			# 	"headspeed" : d, 
			# 	"stepLength": 10}, 
			# 20: {"mini":[maxX-50, 0], 
			# 	"maxi": [maxX, 50],
			# 	"headspeed" : e, 
			# 	"stepLength": 5},
			# # Full bed coverage 
			# 21: {"mini":[0, 0], 
			# 	"maxi": [maxX, maxY], 
			# 	"headspeed" : 6000, 
			# 	"stepLength": 20},
			# 22: {"mini":[maxX/2 - 25, maxY/2 -25], 
			# 	"maxi": [maxX/2 + 25, maxY/2 +25], 
			# 	"headspeed" : 6000, 
			# 	"stepLength": 5},

}	