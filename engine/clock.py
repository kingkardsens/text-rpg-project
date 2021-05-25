# a clock to simulate in game time in a text rpg

# stuff left: None


class Clock:
	def __init__(self, time=0, tickrate=1, day=1, phases=[], phaseindex=0, phaserate=20):
		self.totaltime = time
		self.time = time
		
		self.tickrate = tickrate 
		self.phases = phases or ['morning','afternoon','evening','night']
		self.phaseindex = phaseindex
		self.phaserate = phaserate 

		self.day = day
		self.dayrate = self.phaserate*len(self.phases)
		 

	@property
	def phase(self):
		return self.phases[self.phaseindex]


	def tick(self,amount=1):
		for i in range(amount):
			self.time += self.tickrate
			self.totaltime += self.tickrate
			if self.time >= self.dayrate: # if day over, inc day and set time to 0 
				self.day += 1
				self.time = 0
				self.phaseindex = 0
			elif self.time % self.phaserate == 0: # if time of day ends change time of day
				self.phaseindex += 1
				if self.phaseindex > len(self.phases)-1:
					self.phaseindex = 0
				

	def reset(self):
		self.time = 0
		self.totaltime = 0
		self.day = 0
		self.phaseindex = 0

	def set(self, values={}):
		for param in values.keys():
			setattr(self, param, values[param])

	def stats(self):
		print(f' TIME: {self.time}/{self.dayrate}, DAY: {self.day}, TIME OF DAY: {self.phase}, TOTAL TIME: {self.totaltime}')

if __name__ == '__main__':
	clock = Clock()
	clock.tick()
	clock.stats()
	

