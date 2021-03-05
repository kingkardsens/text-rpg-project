# entity system

import random

class Entity:
	def __init__(self, name, hp, mp=0, attacks=[], ispattern=False, discovery_lines=None, drops={}): # drops = {'bones':(min,max)}
		self.name = name.strip().upper()
		self.hp = hp
		self.mhp = hp
		self.mp = mp
		self.mmp = mp
		self.statuseffect = None
		self.discovery_lines = discovery_lines or 'you crossed paths with a '+self.name+'!'
		self.line = None 			# line displayed after every attack
		self.attacks = attacks

		self.ispattern = ispattern
		self.currentattackindex = 0

		self.drops = drops

	@property
	def currentattack(self):
		return attacks[self.currentattackindex]
	

	def heal(self, amount):
		self.hp+=amount
		if self.hp > self.mhp:
			self.hp = self.mhp

	def damage(self, amount):
		self.hp-=amount
		if self.hp < 0:
			self.hp = 0

	def getdrop(self):
		drop = random.choice(list(self.drops.keys()))
		amount = random.randint(self.drops[drop][0],self.drops[drop][1])
		return (drop, amount)

	def reset(self):
		self.hp = self.mhp
		self.mp = self.mmp
		self.currentattackindex = 0

	
	def setstatus(self, value):
		self.statuseffect = value

	def removestatus(self):
		self.statuseffect = None

	def attack(self, other, index_=False):
		if not index_:
			if self.ispattern:
				value = self.attacks[self.currentattackindex](self, other)
				self.currentattackindex+=1
				if self.currentattackindex > len(self.attacks)-1:
					self.currentattackindex = 0
			else:
				value = random.choice(self.attacks)(self, other)
		else:
			value = self.attacks[index_](self, other)
		return value

	def die(self):
		if self.hp < 0:
			self.reset()
			return self.getdrop()


class Boss(Entity):
	def __init__(self, name, hp, mp, attacks, discovery_lines, drops):
		super().__init__(name, hp, mp, attacks, ispattern=True, discovery_lines=discovery_lines, drops=drops)
		

	

		


