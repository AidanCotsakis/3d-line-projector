import pygame
import math
import os
import time

pygame.init()
clock = pygame.time.Clock()
fps = 120

windowSize = [1920, 1080]

os.environ['SDL_VIDEO_CENTERED'] = '1'
win = pygame.display.set_mode(windowSize, pygame.NOFRAME, 0)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

# forward, left, back, right, up, down
inputs = [False, False, False, False, False, False]

def matrixMultiplication(matrix1, matrix2):
	# Check if matrices are valid
	matrix1Dimensions = [len(matrix1[0]),len(matrix1)]
	matrix2Dimensions = [len(matrix2[0]),len(matrix2)]

	if matrix1Dimensions[0] != matrix2Dimensions[1]:
		return

	for i in matrix1:
		if len(i) != matrix1Dimensions[0]:
			return

	for i in matrix2:
		if len(i) != matrix2Dimensions[0]:
			return

	# multiply if valid
	matrix3 = []

	for i in range(matrix1Dimensions[1]):
		
		matrixLine = []
		for j in range(matrix2Dimensions[0]):
			
			value = 0
			for k in range(matrix1Dimensions[0]):
				value += matrix1[i][k] * matrix2[k][j]
			matrixLine.append(value)

		matrix3.append(matrixLine)

	return matrix3

class player(object):
	def __init__(self, coords):
		self.coords = coords
		self.height = 1.8
		self.rotation = [0,0,0]
		self.sensitivity = 0.001
		self.speed = 0.05

	def rotate(self, movement):
		self.rotation = [self.rotation[0]+movement[1]*self.sensitivity, self.rotation[1]+movement[0]*self.sensitivity, self.rotation[2]]
		if self.rotation[0] > math.pi/2:
			self.rotation = [math.pi/2, self.rotation[1], self.rotation[2]]
		elif self.rotation[0] < -math.pi/2:
			self.rotation = [-math.pi/2, self.rotation[1], self.rotation[2]]

	def move(self, inputs):
		direction = False

		if inputs[0:4] == [1,0,0,0]: direction = math.pi*2
		elif inputs[0:4] == [1,0,0,1]: direction = math.pi*1/4
		elif inputs[0:4] == [0,0,0,1]: direction = math.pi*1/2
		elif inputs[0:4] == [0,0,1,1]: direction = math.pi*3/4
		elif inputs[0:4] == [0,0,1,0]: direction = math.pi
		elif inputs[0:4] == [0,1,1,0]: direction = math.pi*5/4
		elif inputs[0:4] == [0,1,0,0]: direction = math.pi*3/2
		elif inputs[0:4] == [1,1,0,0]: direction = math.pi*7/4

		if direction != False:
			angle = self.rotation[1] + direction
			displacement = [self.speed*math.sin(angle), -self.speed*math.cos(angle)]
			print(displacement, angle, math.sin(angle), math.cos(angle))
			self.coords = [self.coords[0] + displacement[0], self.coords[1], self.coords[2] + displacement[1]]

		verticle = 0
		if inputs[4]:
			verticle += self.speed
		if inputs[5]:
			verticle -= self.speed

		if verticle:
			self.coords = [self.coords[0], self.coords[1]+verticle, self.coords[2]]

class object3D(object):
	def __init__(self, coords):
		self.coords = coords # X, Y, Z
		self.dimensions = [1,1,1] # X, Y, Z

		self.colour = (200,0,0)

		self.offset = [0,0,0]

		self.pixels = windowSize
		self.sensor = [windowSize[0]/10000, windowSize[1]/10000]
		self.focal = 0.1
		self.skew = 0

		self.generateCuboid()

	def generateCuboid(self):
		self.points3D = [
		[self.coords[0], self.coords[1], self.coords[2]],
		[self.coords[0], self.coords[1], self.coords[2] + self.dimensions[2]],
		[self.coords[0] + self.dimensions[0], self.coords[1], self.coords[2] + self.dimensions[2]],
		[self.coords[0] + self.dimensions[0], self.coords[1], self.coords[2]],
		[self.coords[0], self.coords[1] + self.dimensions[1], self.coords[2]],
		[self.coords[0], self.coords[1] + self.dimensions[1], self.coords[2] + self.dimensions[2]],
		[self.coords[0] + self.dimensions[0], self.coords[1] + self.dimensions[1], self.coords[2] + self.dimensions[2]],
		[self.coords[0] + self.dimensions[0], self.coords[1] + self.dimensions[1], self.coords[2]]]

		self.edges = [
		[0,1],
		[1,2],
		[2,3],
		[0,3],
		[0,4],
		[1,5],
		[2,6],
		[3,7],
		[4,5],
		[5,6],
		[6,7],
		[4,7]]

	def updateData(self, player):
		self.edges = []
		self.faces = []
		# top
		if player.coords[1]+player.height > self.coords[1]+self.dimensions[1]:
			if [4,5] not in self.edges: self.edges.append([4,5])
			if [5,6] not in self.edges: self.edges.append([5,6])
			if [6,7] not in self.edges: self.edges.append([6,7])
			if [4,7] not in self.edges: self.edges.append([4,7])
			self.faces.append([4,5,6,7])

		# bottom
		if player.coords[1]+player.height < self.coords[1]:
			if [0,1] not in self.edges: self.edges.append([0,1])
			if [1,2] not in self.edges: self.edges.append([1,2])
			if [2,3] not in self.edges: self.edges.append([2,3])
			if [0,3] not in self.edges: self.edges.append([0,3])
			self.faces.append([0,1,2,3])

		# north
		if player.coords[2] > self.coords[2]+self.dimensions[2]:
			if [1,2] not in self.edges: self.edges.append([1,2])
			if [1,5] not in self.edges: self.edges.append([1,5])
			if [5,6] not in self.edges: self.edges.append([5,6])
			if [2,6] not in self.edges: self.edges.append([2,6])
			self.faces.append([1,5,6,2])

		# south
		if player.coords[2] < self.coords[2]:
			if [0,3] not in self.edges: self.edges.append([0,3])
			if [0,4] not in self.edges: self.edges.append([0,4])
			if [4,7] not in self.edges: self.edges.append([4,7])
			if [3,7] not in self.edges: self.edges.append([3,7])
			self.faces.append([0,4,7,3])

		# west
		if player.coords[0] < self.coords[0]:
			if [0,1] not in self.edges: self.edges.append([0,1])
			if [0,4] not in self.edges: self.edges.append([0,4])
			if [4,5] not in self.edges: self.edges.append([4,5])
			if [1,5] not in self.edges: self.edges.append([1,5])
			self.faces.append([0,1,5,4])

		# east
		if player.coords[0] > self.coords[0]+self.dimensions[0]:
			if [2,3] not in self.edges: self.edges.append([2,3])
			if [3,7] not in self.edges: self.edges.append([3,7])
			if [6,7] not in self.edges: self.edges.append([6,7])
			if [2,6] not in self.edges: self.edges.append([2,6])
			self.faces.append([3,2,6,7])

		middle = [self.coords[0]+self.dimensions[0]/2,self.coords[1]+self.dimensions[1]/2,self.coords[2]+self.dimensions[2]/2]

		distance = math.sqrt( (middle[0]-player.coords[0])**2 + (middle[1]-(player.coords[1]+player.height))**2 + (middle[2]-player.coords[2])**2 )

		return [distance, self.faces, self.edges, self.translate(player), self.colour]


	def translate(self, player):

		windowFix = [
		[1, 0, 0, windowSize[0]/2],
		[0, -1, 0, windowSize[1]/2],
		[0, 0, 1, 0],
		[0, 0, 0, 1]]

		a = [
		[(self.focal*windowSize[0])/(2*self.sensor[0]), self.skew, 0, 0],
		[0, (self.focal*windowSize[1])/(2*self.sensor[1]), 0, 0],
		[0, 0, -1, 0],
		[0, 0, 0, 1]]

		b = [
		[1, 0, 0, -self.offset[0]],
		[0, 1, 0, -self.offset[1]],
		[0, 0, 1, -self.offset[2]],
		[0, 0, 0, 1]]

		c = [
		[1, 0, 0, 0],
		[0, math.cos(player.rotation[0]), -math.sin(player.rotation[0]), 0],
		[0, math.sin(player.rotation[0]), math.cos(player.rotation[0]), 0],
		[0, 0, 0, 1]]

		d = [
		[math.cos(player.rotation[1]), 0, math.sin(player.rotation[1]), 0],
		[0, 1, 0, 0],
		[-math.sin(player.rotation[1]), 0, math.cos(player.rotation[1]), 0],
		[0, 0, 0, 1]]

		e = [
		[math.cos(player.rotation[2]), -math.sin(player.rotation[2]), 0, 0],
		[math.sin(player.rotation[2]), math.cos(player.rotation[2]), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]]

		f = [
		[1, 0, 0, -player.coords[0]],
		[0, 1, 0, -(player.coords[1]+player.height)],
		[0, 0, 1, -player.coords[2]],
		[0, 0, 0, 1]]

		multiplierMatrix = matrixMultiplication(a, b)
		multiplierMatrix = matrixMultiplication(multiplierMatrix, c)
		multiplierMatrix = matrixMultiplication(multiplierMatrix, d)
		multiplierMatrix = matrixMultiplication(multiplierMatrix, e)
		multiplierMatrix = matrixMultiplication(multiplierMatrix, f)

		points2D = []
		for point in self.points3D:
			point = [[point[0]],[point[1]],[point[2]],[1]]
			
			orthographicPoint = matrixMultiplication(multiplierMatrix, point)

			if orthographicPoint[2][0] != 0:
				perspectiveMatrix = [
				[1/orthographicPoint[2][0], 0, 0, 0],
				[0, 1/orthographicPoint[2][0], 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]]

				perspectivePoint = matrixMultiplication(perspectiveMatrix, orthographicPoint)
				perspectivePoint = matrixMultiplication(windowFix, perspectivePoint)
			else:
				perspectivePoint = orthographicPoint

			points2D.append(perspectivePoint)

		return points2D

cubes = [
object3D([0,0,0]),
object3D([-2,0,0]),
object3D([2,0,0]),
object3D([4,0,0]),
object3D([-4,0,0])
]

def draw():
	win.fill((255,255,255))

	cubesData = []
	for cube in cubes:
		# [distance, faces, edges, points, colour]
		cubeData = cube.updateData(player)
		cubesData.append(cubeData)

	cubesData = sorted(cubesData)
	cubesData.reverse()

	for cube in cubesData:
		for edge in cube[2]:
			if cube[3][edge[0]][2][0] > 0 and cube[3][edge[1]][2][0] > 0:
				pygame.draw.line(win, (0,0,0), (cube[3][edge[0]][0][0], cube[3][edge[0]][1][0]), (cube[3][edge[1]][0][0], cube[3][edge[1]][1][0]), 2)


	pygame.display.update()

player = player([0.5,2,3])
player.rotation[0] = 0.5
angle = 0
rotate_point = [0.5,0.5]

while True:
	time.sleep(0.02)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		
		if event.type == pygame.MOUSEMOTION:
			mouse_position = pygame.mouse.get_pos()
			movement = [mouse_position[0]-windowSize[0]/2, mouse_position[1]-windowSize[1]/2]
			pygame.mouse.set_pos(windowSize[0]/2, windowSize[1]/2)
			player.rotate(movement)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == ord('w'):
				inputs[0] = True
			if event.key == pygame.K_LEFT or event.key == ord('a'):
				inputs[1] = True
			if event.key == pygame.K_DOWN or event.key == ord('s'):
				inputs[2] = True
			if event.key == pygame.K_RIGHT or event.key == ord('d'):
				inputs[3] = True
			if event.key == pygame.K_SPACE:
				inputs[4] = True
			if event.key == pygame.K_LSHIFT:
				inputs[5] = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == ord('w'):
				inputs[0] = False
			if event.key == pygame.K_LEFT or event.key == ord('a'):
				inputs[1] = False
			if event.key == pygame.K_DOWN or event.key == ord('s'):
				inputs[2] = False
			if event.key == pygame.K_RIGHT or event.key == ord('d'):
				inputs[3] = False
			if event.key == pygame.K_SPACE:
				inputs[4] = False
			if event.key == pygame.K_LSHIFT:
				inputs[5] = False

	player.move(inputs)

	draw()