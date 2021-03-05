import random

class Location:
	def __init__(self,envlist,seed=1,location=[0,0]):
		self.location = location
		self.string = None
		self.envlist = envlist
		self.seed = seed
		self.convert_location()

	def convert_location(self,location=0):
		if location != 0:
			string = str(location[0]+self.seed)+str(location[0])+str(location[1]+self.seed)+str(location[1])
			return string
		else:

			self.string = str(self.location[0]+self.seed) + str(self.location[0]) + str(self.location[1]+self.seed) + str(self.location[1])

	def change_location(self, direction, magnitude=1,coordinates=None):
		if not coordinates:
			x = self.location[0]
			y = self.location[1]
		else:
			x = coordinates[0]
			y = coordinates[1]
		if direction == 'up': y+=magnitude
		elif direction == 'down': y-=magnitude			
		elif direction == 'left': x-=magnitude			
		elif direction == 'right': x+=magnitude
			

		return (x,y)

	def move(self,direction,magnitude=1):
		if type(direction) is not tuple:
			x,y = self.change_location(direction,magnitude)[0],self.change_location(direction,magnitude)[1]
		else:
			x = direction[0]
			y = direction[1]

		self.location[0] = x
		self.location[1] = y
		self.convert_location()

	def display(self):

		print('root seed:',self.seed)
		print('location:',self.location,'quadrant',self.find_quadrant())
		print('seed:',self.string)


	def generate(self, string=0):
		if string != 0:
			random.seed(string)
		else:
			random.seed(self.string)
		env = random.choice(self.envlist)
		return env

	def surroundings_dict(self,radius=7):
		
		all_points = {}
		all_points['y'] = {}
		for direction in ['up','down']:
			all_points['y'][direction] = {}
			for i in range(1,radius):			
				yaxis_point = self.change_location(direction,i)
				all_points['y'][direction][yaxis_point] = {}
		
		for ydir in ['up','down']:
			for point in all_points['y'][ydir].keys():
				for direction in ['left','right']:	
					all_points['y'][ydir][point][direction] = []

					for i in range(1,radius):
						all_points['y'][ydir][point][direction].append(self.change_location(direction,i,point))

		all_points['y']['center'] = {tuple(self.location):{}}
		
		for direction in ['left','right']:
			all_points['y']['center'][tuple(self.location)][direction] = []
			for i in range(1,radius):
				all_points['y']['center'][tuple(self.location)][direction].append(self.change_location(direction,i))
		
		


		return all_points

	def surroundings_table(self,radius=7):
		all_points = self.surroundings_dict(radius)
		table = []
		for axis in all_points.keys():
			rownum = 0
			for ydirection in ['up','center','down']:
				point_in_direction = all_points[axis][ydirection].keys()
				if ydirection=='up':
					point_in_direction = list(point_in_direction)
					point_in_direction.reverse()
				for point in point_in_direction:
					table.append([])
					#for direction in all_points[axis][ydirection][point].keys():
					left = all_points[axis][ydirection][point]['left']
					left.reverse()
					table[rownum].extend(left)
					table[rownum].append(point)
					table[rownum].extend(all_points[axis][ydirection][point]['right'])
					rownum+=1
		return table


	def surroundings(self,radius=7,show_coords=False):
		radius-=1
		table = self.surroundings_table(radius)
		name_table = []
		rownum = 0
		for row in table:
			name_table.append([])
			for col in row:
				name_table[rownum].append(self.generate(self.convert_location(col))) # generate environment and append
			rownum+=1
		
		index = (radius + (radius-1))//2
		name_table[index][index] = name_table[index][index].name.upper()

		if show_coords:
			print('       ',end='')
			for col in table[0]:
				length = 8-len(str(col[0]))
				print(col[0],end=' '*length)
			print()
		#print()
		for row in name_table:
			if show_coords:
				length = 5-len(str(table[name_table.index(row)][0][1]))
				print('',table[name_table.index(row)][0][1],end=' '*length)
			for col in row:
				try:
					print(col.name,end=' ')
				except:
					print(col,end=' ')
			print()
			print()

		return table


	def find_quadrant(self,location=False):
		if not location:
			x = self.location[0]
			y = self.location[1]
		else:
			x = location[0]
			y = location[1]

		quadrant = None

		if x<0 and y<0: quadrant = 3
		elif x<0 and y>0: quadrant = 2			
		elif x>0 and y<0: quadrant = 4			
		elif x>0 and y>0: quadrant = 1
			

		return quadrant
		












'''

class Cell:
	def __init__(self):
		self.cell = ' '
		self.player = False
class Dungeon:
	def __init__(self,dimensions=(60,30),minrooms=3,maxrooms=7,minside=4,maxside=15):
		self.dimensions = dimensions
		self.minrooms = minrooms
		self.maxrooms = maxrooms
		self.minside = minside
		self.maxside = maxside
		self.tiles = {'floor':'#','wall':':','blank':' '}
		self.roomlist = []
		self.table = []
		
	def generate_room(self):
		
		w = random.randint(self.minside,self.maxside)
		h = random.randint(self.minside,self.maxside)
		x = 1
		y = 1
		room = [(x,y+h),(x+w,y),w,h]
		return room

	def check_overlap(self,room,room2):
		x1 = room[1][0]
		y1 = room[1][1]
		w1 = room[2]
		h1 = room[3]

		x2 = room2[1][0]
		y2 = room2[1][1]
		w2 = room2[2]+2
		h2 = room2[3]+2

		if x1<x2+w2 and x2<x1+w1 and y1<y2+h2 and y2<y1+h1:
			#print('OVERLAP')
			#print((x1,y1),w1,h1,'',(x2,y2),w2,h2)
			return True
		else:
			#print('DONT OVERLAP')
			#print((x1,y1),w1,h1,'',(x2,y2),w2,h2)
			return False


	def position_room(self,room):

		w2 = room[2]
		h2 = room[3]
					
		x2 = random.randint(w2+1,self.dimensions[0]-1)
		y2 = random.randint(0,self.dimensions[1]-1-h2)
		
		return [None, (x2,y2),w2,h2]

	def final_overlap_check(self):
		for room in self.roomlist:
			for other_room in self.roomlist:
				if room == other_room:
					continue
				if self.check_overlap(room, other_room) == True:
					return False
		return True

	def print_dungeon(self):

		
		for row in self.table:
		
			for col in row:
				print(col.cell,end='')
			print()

	def set_dungeon(self):
		for i in range(0,5):
			tmp_room = self.generate_room
			if tmp_room:
				tmp_room = self.position_room(tmp_room)
				for current_room in self.roomlist:
					if self.check_overlap(tmp_room,current_room) == False:
						self.set_dungeon()
					else:
						self.roomlist.append(room)
						continue


		w = self.dimensions[0]
		h = self.dimensions[1]

		for row in range(h):
			self.table.append([])
			for col in range(w):
				cell = Cell()
				self.table[row].append(cell)

		self.replace_cells()
		print(self.final_overlap_check())
		

	def room_area_coords(self,room):
		x,y,w,h = room[1][0],room[1][1],room[2],room[3]
		
		area = [[],[]]
		for i in range(0,h):
			for j in range(0,w):
				coords = (x-j,y+i)
				if j == 0 or j == w-1 or i == 0 or i == h-1:
					area[0].append(coords)
				else:
					area[1].append(coords)


		return area



	def replace_cells(self):
		
		for room in self.roomlist:
			area_table = self.room_area_coords(room)

			for area in area_table:
				for coord in area:
					x,y = coord[0],coord[1]
					
					if area_table.index(area) == 0:
						self.table[len(self.table)-1-y][x-1].cell = '#'
					else:
						self.table[len(self.table)-1-y][x-1].cell = '#'
		self.print_dungeon()
		


d = Dungeon()
d.set_dungeon()
		



{
	'y': {
			'up': {


					(0, 1): {
								'left': [(-1, 1), (-2, 1), (-3, 1), (-4, 1), (-5, 1)],
								'right': [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
								}, 
					(0, 2): {
								'left': [(-1, 2), (-2, 2), (-3, 2), (-4, 2), (-5, 2)], 
								'right': [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
								}, 
					(0, 3): {
								'left': [(-1, 3), (-2, 3), (-3, 3), (-4, 3), (-5, 3)], 
								'right': [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)]
								}, 
					(0, 4): {
								'left': [(-1, 4), (-2, 4), (-3, 4), (-4, 4), (-5, 4)], 
								'right': [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4)]
								}, 
					(0, 5): {
								'left': [(-1, 5), (-2, 5), (-3, 5), (-4, 5), (-5, 5)], 
								'right': [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]
								}


									}, 

			'down': {



					(0, -1): {
								'left': [(-1, -1), (-2, -1), (-3, -1), (-4, -1), (-5, -1)], 
								'right': [(1, -1), (2, -1), (3, -1), (4, -1), (5, -1)]
								}, 
					(0, -2): {
								'left': [(-1, -2), (-2, -2), (-3, -2), (-4, -2), (-5, -2)], 
								'right': [(1, -2), (2, -2), (3, -2), (4, -2), (5, -2)]
								}, 
					(0, -3): {
								'left': [(-1, -3), (-2, -3), (-3, -3), (-4, -3), (-5, -3)], 
								'right': [(1, -3), (2, -3), (3, -3), (4, -3), (5, -3)]
								}, 
					(0, -4): {
								'left': [(-1, -4), (-2, -4), (-3, -4), (-4, -4), (-5, -4)], 
								'right': [(1, -4), (2, -4), (3, -4), (4, -4), (5, -4)]
								}, 
					(0, -5): {
								'left': [(-1, -5), (-2, -5), (-3, -5), (-4, -5), (-5, -5)], 
								'right': [(1, -5), (2, -5), (3, -5), (4, -5), (5, -5)]
								}


									},

			'center': {

					(0, 0): {
								'left': [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0)], 
								'right': [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
								}



									}
										}
											}




[
	[(-5, 1), (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)], 
	[(-5, 2), (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)], 
	[(-5, 3), (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3)], 
	[(-5, 4), (-4, 4), (-3, 4), (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4)], 
	[(-5, 5), (-4, 5), (-3, 5), (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)], 
	[(-5, 0), (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], 
	[(-5, -1), (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1)], 
	[(-5, -2), (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2)], 
	[(-5, -3), (-4, -3), (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3), (5, -3)], 
	[(-5, -4), (-4, -4), (-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), (3, -4), (4, -4), (5, -4)], 
	[(-5, -5), (-4, -5), (-3, -5), (-2, -5), (-1, -5), (0, -5), (1, -5), (2, -5), (3, -5), (4, -5), (5, -5)]
		]



'''

































'''
class Map:
	def __init__(self, seed, environments, grid_size=3):
		self.player_coords = (1,2)
		self.seed = seed
		self.environments = environments
		self.grid_size = grid_size
		self.current_map = []
		self.generate_map()

	def generate_map(self):
		self.current_map = []
		random.seed(self.seed)
		for i in range(0,self.grid_size):
			self.current_map.append([])
			for j in range(0,self.grid_size):
				env = random.choice(list(self.environments.keys()))
				self.current_map[i].append(env)

	def print_map(self):
		index = 0
		size = self.grid_size-1
		rownum = 0
		
		for row in self.current_map:
			boxnum = 0
			for box in row:
				if index % size != 0 or index == 0:
					if rownum == self.grid_size//2 and boxnum == self.grid_size//2:
						print(box.upper(),end=' ')
					else:
						print(box,end=' ')
				else:
					print(box)
					print()
					index = -1
				index+=1
				boxnum+=1
			rownum+=1

	def get_player_loc(self):
		
		x = self.player_coords[0]
		y = self.player_coords[1]
		player_loc = (x,y)

		center_x=self.grid_size//2
		center_y=self.grid_size//2
		center = (center_x,center_y)
		
		print(player_loc)

a = Map('seed',{'village':village,'forest':None},9)

#print(a.current_map)
a.print_map()
a.get_player_loc()




# 3x3 0,1 --> 2,1
# 9x9 0,1 --> 5,4
'''