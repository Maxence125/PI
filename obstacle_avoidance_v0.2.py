#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import matplotlib.pyplot as plt



PORT_NAME = '/dev/ttyUSB0'


def run():
	'''Main function'''
	lidar = RPLidar(PORT_NAME)
	data = []
	angles = []
	distances = []
	k = 0





	print('-----')
	for scan in lidar.iter_scans('express'):

		scan = np.array(scan)
					
		angle = np.deg2rad(360-scan[0][1])
		distance = scan[0][2]
			
			
		if ((angle < 1.09) | (angle > 5.18)) & (distance < 400) : #+/- 63°
			print('1')
		elif ((angle < 0.46) | (angle > 5.81)) & (distance < 800) : #+/- 26.56°
			print('2')
		elif ((angle < 0.36) | (angle > 5.89)) & (distance < 1000) : #+/- 21.81°
			print('3')
		elif ((angle < 0.24) | (angle > 6.02)) & (distance < 1500) : #+/- 14.93°
			print('4')
		elif ((angle < 0.19) | (angle > 6.07)) & (distance < 2000) : #+/- 11.30°
			print('5')
		elif ((angle < 0.15) | (angle > 6.10)) & (distance < 2500) : #+/- 9.09°
			print('6')
		elif ((angle < 0.13) | (angle > 6.14)) & (distance < 3000) : #+/- 7.59° 
			print('7')
			
			
		k += 1
		if k == 1 :
			break

	lidar.stop()
	lidar.disconnect()
	#np.save(path, np.array(data))
	
	

while True :
	run()

