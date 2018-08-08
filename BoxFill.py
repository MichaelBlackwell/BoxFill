import random, sys, csv, numpy
from PIL import Image 
from numba import jit, int32

import time
mils = int(round(time.time() * 1000))

M = int(sys.argv[1])
N = int(sys.argv[2])
r = int(sys.argv[3])

grid = numpy.zeros((M,N,r))

maxBoxSizeX = 5
maxBoxSizeY = 5
maxBoxSizeZ = r

#start the count
count = []
for i in range(0, r):
	count.append(0)


im = Image.open('england.jpg')
pix = im.load()

# Obtain the value of a pixel every box witdth/height from the heightmap.
for Y in range(0,M):
	for X in range(0,N):
		#if the height of the cube is less than the height of the fillgrid, have that filled space contain a 1, otherwise 0
		xpic = int(X/M*im.size[0])
		ypic = int(Y/N*im.size[1])
		value = pix[xpic,ypic][0]

		#if the height of the cube is less than the height given by its heightmap value, have that filled space contain a 1, otherwise 0
		temp = int32(value * r / 255) + 1
		grid[X][Y][0:temp - 1] = 1
		grid[X][Y][temp:r] = 0
		 
		#count[int(grid[X][Y])-1] += 1

# go through every size box and try to find the one that fits and has the largest volume and fits.
# return its size and location and if a box was found

@jit(nopython=True)
def custom_convolution(A,B,tb):

	dimA = A.shape
	dimB = B.shape
	tempVolume = dimA[0] * dimA[1] * dimA[2]

	# check every position inside grid[][][] where the box would fit
	for containerX in range(0, dimB[0] - dimA[0] + 1):
		for containerY in range(0, dimB[1] - dimA[1] + 1):
			for containerZ in range(0, dimB[2] - dimA[2] + 1):

				#check each spot in box and compare it to the value in filled box
				# if all are 1, then the box is valid

				valid = True

				for insideX in range(containerX, dimA[0] + containerX):
					for insideY in range(containerY, dimA[1] + containerY):
						for insideZ in range(containerZ, dimA[2] + containerZ):
							
							
							if(B[insideX][insideY][insideZ] != 1):
								valid = False
								break
								break
								break
							
				# if this is the largest box, save the size and location in tb[]
				if(valid and tempVolume > tb[0]):
					
					tb[0] = tempVolume
					tb[1] = containerX
					tb[2] = containerY
					tb[3] = containerZ
					tb[4] = dimA[0]
					tb[5] = dimA[1]
					tb[6] = dimA[2]
					tb[7] = 1
					
					# print("largestVolume: " + str(largestVolume))
	return tb
	
lb = numpy.zeros((8,), dtype=numpy.int)

with open('Largestcubes.csv', 'w') as csvfile:
	# Format line check
	csvfile.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
	csvfile.write("\n")
	lb[0] = 1
	while lb[0] != 0:

		lb[0:7] = 0

		#go through every size box possible
		for tempSizeX in reversed(range(1,maxBoxSizeX)):
			for tempSizeY in reversed(range(1,maxBoxSizeY)):
				for tempSizeZ in reversed(range(1,maxBoxSizeZ)):

					tempGrid = numpy.ones((tempSizeX,tempSizeY,tempSizeZ))

					# Call the custom_convolution function using GPU speedup
					lb = custom_convolution(tempGrid, grid, lb)

					
		# Display the largest box to the console
		print( "")
		print( "Largest: " + str(lb[0]))
		print( "X: " + str(lb[1]))
		print( "Y: " + str(lb[2]))
		print( "Z: " + str(lb[3]))
		print( "SizeY: " + str(lb[4]))
		print( "SizeX: " + str(lb[5]))
		print( "SizeZ: " + str(lb[6]))

		# record the largest box's 8 vertices 
		if lb[7] and lb[0] > 0:
			csvfile.write(str(lb[0]) + 			",")
			csvfile.write(str(lb[1]) + 			"," + str(lb[2]) + 			"," + str(lb[3]) + ",")
			csvfile.write(str(lb[1]) + 			"," + str(lb[2] + lb[5]) +  "," + str(lb[3]) + ",")
			csvfile.write(str(lb[1] + lb[4]) +  "," + str(lb[2]) + 			"," + str(lb[3]) + ",")
			csvfile.write(str(lb[1] + lb[4]) +  "," + str(lb[2] + lb[5]) +  "," + str(lb[3]) + ",")

			csvfile.write(str(lb[1]) + 			"," + str(lb[2]) + 			"," + str(lb[3] + lb[6]) + ",")
			csvfile.write(str(lb[1]) + 			"," + str(lb[2] + lb[5]) +  "," + str(lb[3] + lb[6]) + ",")
			csvfile.write(str(lb[1] + lb[4]) +  "," + str(lb[2]) + 			"," + str(lb[3] + lb[6]) + ",")
			csvfile.write(str(lb[1] + lb[4]) +  "," + str(lb[2] + lb[5]) +  "," + str(lb[3] + lb[6]))
			csvfile.write("\n")	

		#update grid with empty space from largest box position
		
		for x in range(lb[1], lb[1] + lb[4]):
			for y in range(lb[2], lb[2] + lb[5]):
				for z in range(lb[3], lb[3] + lb[6]):
					grid[x][y][z] = 0
							
aftermils = int(round(time.time() * 1000))
totaltime = aftermils - mils
print ("time in seconds: ", totaltime / 1000)

# def checkValid (a, b):


