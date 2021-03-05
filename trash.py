
def movement_handler(self):
	coords = self.coords

	def move_sequence(direction):
		direction = direction[0]
		coords.move(direction)
		

	def back():
		return 'stop'

	def display_surroundings():
		coords.display()
		print('-'*90)
		print()
		coords.surroundings(4)

	def enter():
		stop = coords.generate().enter(self)
		return ['return',stop]

	a = Menu({
				'title':'MOVE',
				'options':{
							'enter':[enter,'x'],
							'up':[move_sequence,('up',None),'w'],
							'down':[move_sequence,('down',None),'s'],
							'right':[move_sequence,('right',None),'d'],
							'left':[move_sequence,('left',None),'a'],
							
							},
				'repeat':display_surroundings
								})
	
	val = a.runMenu(end=False)
	try:
		return val[0]
	except TypeError:
		return val

if __name__ == '__main__':
	import engine.clock
