#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import matplotlib.pyplot as plt
from math import sqrt, cos



PORT_NAME = '/dev/ttyUSB0'




seuil_obstacle = 4

def tri_insertion(liste1, liste2):
    L1 = list(liste1) # copie de la liste
    L2 = list(liste2)
    N = len(L1)
    for n in range(1,N):
        cle1 = L1[n]
        cle2 = L2[n]
        j = n-1
        while j>=0 and L1[j] > cle1:
            L1[j+1] = L1[j] # decalage
            L2[j+1] = L2[j]
            j = j-1
        L1[j+1] = cle1
        L2[j+1] = cle2
    return L1, L2


def distancef(angle1, distance1, angle2, distance2) :
    return sqrt(distance1*distance1 + distance2*distance2 - 2*distance1*distance2*cos(angle2-angle1))
 
def run():
	'''Main function'''
	lidar = RPLidar(PORT_NAME)
	angles = []
	distances = []
	k = 0

	angles1 = []; distances1 = []
	angles2 = []; distances2 = []
	angles3 = []; distances3 = []

	angles1m = []; distances1m = []
	angles2m = []; distances2m = []
	angles3m = []; distances3m = []


	print('Recording measurments... Press Crl+C to stop.')
	for scan in lidar.iter_scans('express'):

		scan = np.array(scan)
		for i in range (len(scan)) :
			
			angle = np.deg2rad(360-scan[i][1])
			distance = scan[i][2]
			
			if ((angle < 1.09) | (angle > 5.18)) & (distance < 400) : #+/- 63°
				angles1.append(angle)
				distances1.append(distance)
			elif ((angle < 0.46) | (angle > 5.81)) & (distance < 800) : #+/- 26.56°
				angles1.append(angle)
				distances1.append(distance)
			elif ((angle < 0.36) | (angle > 5.89)) & (distance < 1000) : #+/- 21.81°
				angles1.append(angle)
				distances1.append(distance)
			elif ((angle < 0.24) | (angle > 6.02)) & (distance < 1500) : #+/- 14.93°
				angles2.append(angle)
				distances2.append(distance)
			elif ((angle < 0.19) | (angle > 6.07)) & (distance < 2000) : #+/- 11.30°
				angles2.append(angle)
				distances2.append(distance)
			elif ((angle < 0.15) | (angle > 6.10)) & (distance < 2500) : #+/- 9.09°
				angles3.append(angle)
				distances3.append(distance)
			elif ((angle < 0.13) | (angle > 6.14)) & (distance < 3000) : #+/- 7.59°
				angles3.append(angle)
				distances3.append(distance)

			

			
			
			
			
			else :
				angles.append(angle)
				distances.append(distance)
			
		k += 1
		if k == 1 :
			break

    
	angles1m, distance1m = tri_insertion(angles1, distances1)
	angles2m, distance2m = tri_insertion(angles2, distances2)
	angles3m, distance3m = tri_insertion(angles3, distances3)
	angles_obstacles = []; distances_obstacles = []
	angles_obstacles2 = []; distances_obstacles2 = []
	angles_obstacles3 = []; distances_obstacles3 = []

	
	for i in range (len(angles1m)-seuil_obstacle) :
		cmpt = 0
		for j in range (seuil_obstacle) : 
			if (distancef(angles1m[i+j], distance1m[i+j], angles1m[i+j+1], distance1m[i+j+1]) < 10) :
				cmpt += 1	
		if cmpt == seuil_obstacle-1 :
			for l in range (seuil_obstacle) : 
				angles_obstacles.append(angles1m[i+l])
				distances_obstacles.append(distance1m[i+l])

	for i in range (len(angles2m)-seuil_obstacle) :
		cmpt = 0
		for j in range (seuil_obstacle) : 	
			if (distancef(angles2m[i+j], distance2m[i+j], angles2m[i+j+1], distance2m[i+j+1]) < 20) :
				cmpt += 1
		if cmpt == seuil_obstacle-1 :
			for l in range (seuil_obstacle) : 
				angles_obstacles2.append(angles2m[i+l])
				distances_obstacles2.append(distance2m[i+l])

	for i in range (len(angles3m)-seuil_obstacle) :
		cmpt = 0
		for j in range (seuil_obstacle) : 
			if (distancef(angles3m[i+j], distance3m[i+j], angles3m[i+j+1], distance3m[i+j+1]) < 50) :
				cmpt += 1
		if cmpt == seuil_obstacle-1 :
			for l in range (seuil_obstacle) : 
				angles_obstacles3.append(angles3m[i+l])
				distances_obstacles3.append(distance3m[i+l])


	print(angles_obstacles, distances_obstacles)

	mark = '.'

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='polar')
	ax.scatter(angles_obstacles, distances_obstacles, c='red', marker = mark)
	ax.scatter(angles_obstacles2, distances_obstacles2, c='blue', marker = mark)
	ax.scatter(angles_obstacles3, distances_obstacles3, c='green', marker = mark)
	ax.set_ylim(0,4000)
	plt.savefig("test.png", bbox_inches='tight')
	plt.show()



	print('Stoping.')
	lidar.stop()
	lidar.disconnect()
	#np.save(path, np.array(data))
	
	


run()

