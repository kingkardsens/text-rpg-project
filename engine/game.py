
# stuff left: the levels feel a bit messy, also maybe try coming up with a better name lmao

from .clock import Clock
from .item_system import Stack

import pickle
import random

# inventory -> logic works, work on interface
class Inventory:
	def __init__(self, items=[], gold=0):
		self.items = items
		self.gold = gold
		self.length = len(items)

	def __len__(self):
		return self.length

	def menu(self): # INTERFACE RELATED
		while True:
			print('INVENTORY')
			self.display()
			print()
			print('> "r [item name] [amount]" to remove item')
			print('> "e" exit')
			choice = input('> ').split(' ')
			try:
				if choice[0].lower().strip() == 'r':
					item = self.get_item_with(name=choice[1])
					if not item:
						print('no such item')
						continue
					try:
						amount = int(choice[2])
					except IndexError:
						amount = 1
					except ValueError:
						print('amount to remove must be a number')
						continue

					self.remove_from_stack(item, amount)

				elif choice[0].lower().strip() == 'e' or 'exit':
					break

			except IndexError:
				print('missing arguments')


	def get_item_with(self,name=None): # get item instance from name of item if item exist in inventory
		for stack in self.items:
			if name.strip().lower() == stack.name.lower():
				return stack.item

	def clear(self):
		self.items = [] 
		self.length = 0

	# useless but ill still keep it here
	def total_items(self, count_stacks=True): # total inventory slots occupied that is
		stacks = {}
		for stack in self.items:
			if count_stacks:
				stacks[stack] = True
			else:
				stacks[stack.name] = True
		return len(list(stacks.keys()))

	def get_item_dict(self, item=None): # {item_instance:amount_in_stack}
		all_items = {}
		for stack in self.items:
			if item and stack.item is not item:
				continue
			all_items[stack] = stack.amount
		return all_items

	@property	
	def item_list(self):
		all_items = {}
		for stack in self.items:
			all_items[stack.item] = None
		return list(all_items.keys())

	def display(self, item=None): # interface related
		if item:
			print('sorted for "'+item.name+'"')

		sorted_items = self.get_items(item=item).items()
		if not len(sorted_items):
			print('Empty')
		else:
			for stack, amount in sorted_items:
				print(f'{stack.name}(x{amount})', end=', ')	
			print()
		print()	





	# stack related section

	def add_to_stack(self, item, amount=1): 
		remainder = amount
		for stack in self.items:
			if stack.item is item:
				if stack.isfull:
					continue
				else:
					remainder = stack.add(amount)
		if remainder:
			remainder = self.create_stack(item, remainder)
			self.length += 1
		if remainder:
			self.add_to_stack(item, remainder)

	def remove_from_stack(self, item, amount=1): 
		remainder = amount
		for stack in self.items[::-1]:
			if stack.item is item:
				remainder = stack.remove(remainder)
				if remainder or stack.amount==0:
					self.items.remove(stack)
					self.length -= 1
		return remainder


	def retrieve_from_stack(self, item, amount=1): 
		remainder = self.remove_from_stack(item, amount)
		return (item, amount-remainder)


	def create_stack(self, item, amount=1):
		new = Stack(item, 0)
		self.items.append(new)
		return new.add(amount)


# bank
class Bank(Inventory):
	def __init__(self, items=[], gold=0):
		super().__init__(items, gold)

	def menu(self):
		pass



# levels -> works, dont change
class Levels:
	def __init__(self,name,xp=0,level=1,required_xp=None):
		self.name = name
		self.xp = xp
		self.level = level # level 1 and shit like that
		self.required_xp = required_xp or {1:100, 2:130, 3:140, 4:160, 5:200} # to level up

	def update(self):
		required_xp = self.required_xp[self.level]
		if self.xp >= required_xp:    
			if self.level+1 in self.required_xp.keys():
				self.level += 1
				self.xp = 0

	def add_xp(self,xp):
		self.xp += xp
		self.update()



# player
class Player:
	def __init__(self,name,gold=0,location=None,env_list=[],seed=1):

		# general
		self.name = name 
		self.hp = [200,200]
		self.mp = [250,250]
		self.player_level = Levels('player level')
		self.location = location 
		
		# slots
		self.slots={
			'forehand':None,
			'offhand':None,
			'armor':None,
			'dual_wield':False
			}
		
		#combat related
		self.levels = {
			'combat':Levels(name='combat'),
			'magic':Levels(name='magic'),
			'crafting':Levels(name='crafting'),
			'looting':Levels(name='looting'),
			'exploration':Levels(name='exploration'),
			'dungeoneering':Levels(name='dungeoneering'),
			'smithing':Levels(name='smithing'),
			'quest':Levels(name='quest')
			}

		self.status_effect = None
		self.engaged = None
		self.stamina = [100,100]
		self.combat_moves = []
		self.counter = 0
		
		# inventory and bank
		self.inventory = Inventory(gold=gold)
		self.bank = Bank()
		
		# stat points
		self.physical_stats = {'dex':0,'int':0,'str':0,'vit':0}
		self.stat_points = 10

		self.mastery_tree = {'sword':0,'knife':0,'bow':0,'axe':0,'hammer':0}
		self.mastery_points = 1
		
        
	# add xp to general player level
	def add_xp(self,xp):
		self.player_level.xp += xp
		self.player_level.update()

	

	# ITEM RELATED

	def give_item(self, item, amount=1):
		return self.inventory.add_to_stack(item, amount)

	def remove_item(self, item, amount=1):
		return self.inventory.remove_from_stack(item, amount)

	def retrieve_item(self, item, amount=1):
		return self.inventory.retrieve_from_stack(item, amount)


	# combat related section

	def heal(self, amount):
		self.hp[0] += amount
		if self.hp[0] > self.hp[1]: self.hp[0] = self.hp[1]

	def damage(self, amount):
		self.hp[0] -= amount
		if self.hp[0] < 0: self.hp[0] = 0

	def generate_mp(self, amount):
		self.mp += amount
		if self.mp > self.mmp: self.mp = self.mmp		

	def drain_mp(self, amount):
		self.mp -= amount
		if self.mp < 0: self.mp = 0



	# use stuff
	def eat(self, consumable):
		consumable.use(self)

	
	def use_attack(self, attack, on):
		attack(self, on)





	# section for checking stuff, IGNORE IF PANIC ATTACK

	def check_required_stats(self, stats={}): # should be fine tbh
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

	def check_required_levels(self, levels={}): # this is fine dw
		if levels:
			for level in levels.keys():
				if self.levels[level].level < levels[level]:
					return False
			return True
		else: return True

	def check_required_mastery(self, mastery={}): # this is fine dw
		if mastery:
			for topic in mastery:
				if self.mastery_tree[topic] < mastery[topic]:
					return False
			return True

	# trash


	'''
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
	'''


					

class Game:
	def __init__(self,name,gold,seed=0,env_list=[],location=None):
		self.seed = seed
		self.clock = Clock()
		self.player = Player(name,gold,seed=seed,env_list=env_list,location=location)

	def save(self,filename='save'):
		with open('saves\\'+filename+'.sav','wb') as f:
			pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)

	def load(self,filename='save'):	
		with open('saves\\'+filename+'.sav','rb') as f:
			load_game = pickle.load(f)
		self.__dict__.update(load_game)

if __name__ == '__main__':
	game = Game('player',5)




	
	



