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

	angles1 = []; distances1 = []
	angles2 = []; distances2 = []
	angles3 = []; distances3 = []
	angles4 = []; distances4 = []
	angles5 = []; distances5 = []
	angles6 = []; distances6 = []
	angles7 = []; distances7 = []




	print('Recording measurments... Press Crl+C to stop.')
	for scan in lidar.iter_scans('express'):

		scan = np.array(scan)
		for i in range (len(scan)) :
			
			angle = np.deg2rad(360-scan[i][1])
			distance = scan[i][2]
			
			if ((angle < 0.13) | (angle > 6.14)) & (distance < 3000) : #+/- 7.59°
				angles1.append(angle)
				distances1.append(distance)
			elif ((angle < 0.15) | (angle > 6.10)) & (distance < 2500) : #+/- 9.09°
				angles2.append(angle)
				distances2.append(distance)
			elif ((angle < 0.19) | (angle > 6.07)) & (distance < 2000) : #+/- 11.30°
				angles3.append(angle)
				distances3.append(distance)
			elif ((angle < 0.24) | (angle > 6.02)) & (distance < 1500) : #+/- 14.93°
				angles4.append(angle)
				distances4.append(distance)
			elif ((angle < 0.36) | (angle > 5.89)) & (distance < 1000) : #+/- 21.81°
				angles5.append(angle)
				distances5.append(distance)
			elif ((angle < 0.46) | (angle > 5.81)) & (distance < 800) : #+/- 26.56°
				angles6.append(angle)
				distances6.append(distance)
			elif ((angle < 1.09) | (angle > 5.18)) & (distance < 400) : #+/- 63°
				angles7.append(angle)
				distances7.append(distance)
			else :
				angles.append(angle)
				distances.append(distance)
			
		k += 1
		if k == 1 :
			break


	mark = '.'

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='polar')
	ax.scatter(angles, distances, c='grey', marker = mark)
	ax.scatter(angles1, distances1, c='red', marker = mark)
	ax.scatter(angles2, distances2, c='yellow', marker = mark)
	ax.scatter(angles3, distances3, c='cyan', marker = mark)
	ax.scatter(angles4, distances4, c='blue', marker = mark)
	ax.scatter(angles5, distances5, c='black', marker = mark)
	ax.scatter(angles6, distances6, c='green', marker = mark)
	ax.scatter(angles7, distances7, c='magenta', marker = mark)
	
	plt.savefig("test.png", bbox_inches='tight')
	plt.show()
	
	print('Stoping.')
	lidar.stop()
	lidar.disconnect()
	#np.save(path, np.array(data))
	
	


run()

