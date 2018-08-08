import csv
import io
import random as ran

from vpython import *

scene = canvas(title= 'visualization of packed boxes', x = 0, y = 0, width = 600, height = 600, center = vector(30,-30,0), background=vector(0,0,0))


filename = "Largestcubes.csv"
zmin = 0
zmax = 1000000

file = open(filename, newline="")

total = 0
data = []
with file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        data.append(row)
        total += 1
print("Submission file {} read with {} data points".format(filename, len(data)))

count = 0

squash = 3.0
volume = 0
largestVolume = 0
numVolumes = 0
lastVolume = 0

totalVolumes = 19.0

boxSizes = {}

with open('BoxData.csv', 'w') as csvfile:
	with open('Glowscript.csv', 'w') as glowfile:

	

		for row in data:
			volume = int(row[0])

			# print("volume: ", volume)
			# print("largestVolume: ", largestVolume)
			# print("numVolumes: ", numVolumes)

			if volume > largestVolume:
				largestVolume = volume 

			if volume != lastVolume:
				lastVolume = volume
				numVolumes += 1

			x1, x2 = sorted(int(x) for x in set(row[1::3]))
			y1, y2 = sorted(int(x) for x in set(row[2::3]))
			z1, z2 = sorted(int(x) for x in set(row[3::3]))
			if ((zmin is not None and min(z1, z2) < zmin) or
			(zmax is not None and max(z1, z2) > zmax)):
				continue
			count += 1
			xx, yy, zz = x2 - x1, y2 - y1, z2 - z1

			if numVolumes / totalVolumes < 0.4:
				red = 0.0
				green = (numVolumes * 3 / totalVolumes)
				blue = 1.0 - numVolumes * 3 / totalVolumes
			elif numVolumes / totalVolumes > 0.4 and numVolumes / totalVolumes < 0.8:
				red = (numVolumes - (totalVolumes / 3.0)) * 2.0 / totalVolumes
				green = 1.0
				blue = 0.0
			else:
				red = 1.0
				green = 1.0 - (numVolumes  - (totalVolumes * 2.0 / 3.0)) * 3.0 / totalVolumes
				blue = 0.0

			# choose a coloring method and place it last

			#grey for all
			color = vector(0.5, 0.5, 0.5)
			#random colors
			color = vector(ran.uniform(0.0,1.0), ran.uniform(0.0,1.0), ran.uniform(0.0,1.0))
			#color by size
			color = vector(red, green, blue)
			#color by height
			color = vector((z1 + zz) / 10 , (z1 + zz) / 10, (z1 + zz) / 10)



			box(pos=vector(x1 + xx / 2, -(y1 + yy / 2), (z1 + zz / 2 - zmin) / squash), size=vector(xx, yy, zz / squash), color=color)

			if(xx > yy):
				temp = xx
				xx = yy
				yy = temp

			sizeString = str(xx) + "x" + str(yy) + "x" + str(zz)


			if sizeString in boxSizes:
			    boxSizes[sizeString] += 1
			else:
			    boxSizes[sizeString] = 1
				

		for e in boxSizes:
			csvfile.write(str(e) + " = " + str(boxSizes[e]))
			csvfile.write("\n")
print("Cubes shown: ", count)
print("numVolumes: ", numVolumes)

