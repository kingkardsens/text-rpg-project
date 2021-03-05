from .clock import Clock
from .util import Levels
from .item_system import Stack

import pickle
import random

# inventory
class Inventory:
	def __init__(self):
		self.items = []

	def menu(self):
		print('INVENTORY')
		self.display()
		print()
		print('> remove [item name] [amount]')
		input('')

	def clear(self):
		self.items = [] 

	def total_items(self, count_stacks=True): # total inventory slots occupied that is
		stacks = {}
		for stack in self.items:
			if count_stacks:
				stacks[stack] = True
			else:
				stacks[stack.name] = True
		return len(list(stacks.keys()))

	def get_items(self, item=None): # sort items and return dictionary
		all_items = {}
		for stack in self.items:
			if item and stack.item is not item:
				continue
			all_items[stack] = stack.amount
		return all_items

	def display(self, item=None):
		if item:
			print('sorted for "'+item.name+'"')
		for stack, amount in self.get_items(item=item).items():
			print(f'{stack.name}(x{amount})', end=', ')	
		print()	

	# stack related section

	def add_to_stack(self, item, amount=1): # INTERFACE RELATED
		remainder = amount
		for stack in self.items:
			if stack.item is item:
				if stack.isfull:
					continue
				else:
					remainder = stack.add(amount)
		remainder = self.create_stack(item, remainder)
		if remainder:
			self.add_to_stack(item, remainder)

	def remove_from_stack(self, item, amount=1): # INTERFACE RELATED
		remainder = amount
		for stack in self.items[::-1]:
			if stack.item is item:
				remainder = stack.remove(remainder)
				if remainder or stack.amount==0:
					self.items.remove(stack)
		return remainder


	def retrieve_from_stack(self, item, amount=1): # INTERFACE RELATED
		remainder = self.remove_from_stack(item, amount)
		return (item, amount-remainder)


	def create_stack(self, item, amount=1):
		new = Stack(item, 0)
		self.items.append(new)
		return new.add(amount)







# bank
class Bank:
    def __init__(self):
        self.items = []
        self.gold = 0

# player
class Player:
	def __init__(self,name,gold,location=None,env_list=[],seed=1):

		# general
		self.name = name 
		self.hp = 200
		self.mhp = 200 
		self.mp = 250
		self.mmp = 250
		self.xp = 0
		self.level = 1
		self.gold = gold 
		self.location = location 
		
		# slots
		self.slots={
			'forehand':None,
			'offhand':None,
			'armor':None,
			'dual_wield':False
			}
		
		#combat related
		self.levellist = {}
		self.initialiselevels()
		self.statuseffect = None
		self.attack = 10
		self.defense = 10
		self.engaged = None
		self.stamina = 100
		self.maxstamina = 100
		self.combat_options = []
		self.counter = 0
		
		# inventory and bank
		self.inventory = Inventory()
		self.bank = Bank()
		
		# stat points
		self.dex = 0
		self.int = 0
		self.str = 0
		self.vit = 0
		self.stat_points = 10

		self.mastery_tree = {'sword':0,'knife':0,'bow':0,'axe':0,'hammer':0}
		self.mastery_points = 1


	def initialiselevels(self):
		combat = Levels(name='combat',xp=0,level=1)
		magic = Levels(name='magic',xp=0,level=1)
		crafting = Levels(name='crafting',xp=0,level=1)
		looting = Levels(name='looting',xp=0,level=1)
		exploration = Levels(name='exploration',xp=0,level=1)
		dungeoneering = Levels(name='dungeoneering',xp=0,level=1)
		smithing = Levels(name='smithing',xp=0,level=1)
		quest = Levels(name='quest',xp=0,level=1)
		self.levellist = {'combat':combat,'magic':magic,'crafting':crafting,'looting':looting,'exploration':exploration,'dungeoneering':dungeoneering,'smithing':smithing,'quest':quest}

	# inventory related section

		# ITEM RELATED

	def give_item(self, item, amount=1):
		return self.inventory.add_to_stack(item, amount)

	def remove_item(self, item, amount=1):
		return self.inventory.remove_from_stack(item, amount)

	def retrieve_item(self, item, amount=1):
		return self.inventory.retrieve_from_stack(item, amount)


	# combat related section

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.mhp: self.hp = self.mhp

	def damage(self, amount):
		self.hp -= amount
		if self.hp < 0: self.hp = 0

	def eat(self, consumable):
		consumable.use(self)

	def generate_mp(self, amount):
		self.mp += amount
		if self.mp > self.mmp: self.mp = self.mmp		

	def drain_mp(self, amount):
		self.mp -= amount
		if self.mp < 0: self.mp = 0

	def use_attack(self, attack, on):
		if self.check_required_stats(attack.req_stats) and self.check_required_levels(attack.req_lvls):
			if not on: value = attack(self) # just something handy for some circumstances
			else: value = attack(self, on)
			return value

	def use_combo(self, combo, on):
		if self.check_required_stats(combo.req_stats) and self.check_required_levels(combo.req_lvls):
			value = combo(self, on)
			return value		

	def use_weapon(self, weapon, on):
		# check if weapon in inventory here
		weapon.use(self, on)

	def use_magic(self, magic, on):
		magic.use(self, on)



	# section for checking stuff

	def check_required_stats(self, stats={}):
		if stats:
			for stat in stats.keys():
				try:
					if self.__dict__[stat] < stats[stat]: 
						return False
				except TypeError:
					if self.__dict__[stat] != stats[stat]: 
						return False

			return True
		else:
			return True

	def check_required_levels(self, levels={}):
		if levels:
			for level in levels.keys():
				if self.levellist[level].level < levels[level]:
					return False
			return True
		else: return True

	def check_required_mastery(self, mastery={}):
		if mastery:
			for topic in mastery:
				if self.mastery_tree[topic] < mastery[topic]:
					return False
			return True

					

class Game:
	def __init__(self,name,gold,seed=0,env_list=[],location=None):
		self.seed = seed
		self.clock = Clock()
		self.player = Player(name,gold,seed=seed,env_list=env_list,location=location)

	def save(self,filename='save'):
		with open('..\\saves\\'+filename+'.sav','wb') as f:
			pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)

	def load(self,filename='save'):
		with open('..\\saves\\'+filename+'.sav','rb') as f:
			load_game = pickle.load(f)
		self.__dict__.update(load_game)

if __name__ == '__main__':
	game = Game('',5)




	
	



