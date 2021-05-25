
# stuff left: just looking at this makes me feel like ive missed something, fuck. FIX IT

# item classes, inheriting from Item base class

class Item: # done
	def __init__(self, name, stackable=True, use_function=None, disappear_after_use=True):
		self.name = name
		self.stackable = stackable
		self.use = use_function
		self.disappear_after_use = disappear_after_use # prolly useless

class Weapon(Item): # done
	def __init__(self, info):
		self.info = info
		super().__init__(info['name'], stackable=False, use_function=self.use, disappear_after_use=False)

		self.durability = info['durability']
		self.max_durability = info['durability']
		self.damage = info['damage']
		self.slot = info['slot']
		self.rarity = info['rarity']
		self.wear_down = info['wear_down']
		self.type = info['type']

		try: self.recipe = info['recipe'] # under testing
		except KeyError: self.recipe = None

		try: self.req_stats = info['req_stats']
		except KeyError: self.req_stats = None

		try: self.req_lvls = info['req_lvls']
		except KeyError: self.req_lvls = None
		

	
	def use(self, player, entity):
		try:
			self.info['attack'](player, entity)
		except KeyError:
			entity.damage(self.damage)

	

class Shield(Item): # shield is different from Weapon because it needs to block the attack, the code for that is way different than for a weapon
	def __init__(self):
		super().__init__()

class Magic(Item): # done
	def __init__(self, name, function, toll, affecting_self = False):
		super().__init__(name, stackable=False, use_function=self.use, disappear_after_use=False)
		self.affecting_self = affecting_self
		self.function = function
		self.toll = toll

	def use(self, player, entity):
		if player.mp >= self.toll:
			player.drain_mp(self.toll)
			if self.affecting_self:
				self.function(player)
			else:
				self.function(player, entity)

class Consumable(Item): # done 
	def __init__(self, name, heal_amount, stat_and_maxstat = ('hp','mhp')):
		super().__init__(name, use_function=self.use)
		self.heal_amount = heal_amount
		self.stat_healed = stat_and_maxstat[0]
		self.max_stat = stat_and_maxstat[1]

	def use(self, player):
		player.__dict__[self.stat_healed] += self.heal_amount
		if player.__dict__[self.stat_healed] > player.__dict__[self.max_stat]:
			player.__dict__[self.stat_healed] = player.__dict__[self.max_stat]

class Artifact(Item):
	def __init__(self):
		super().__init__()

class Material(Item):
	def __init__(self):
		super().__init__()

class Currency(Item): # prolly useless
	def __init__(self):
		super().__init__()

class AffectOthers(Item): # item effecting entities
	def __init__(self):
		super().__init__()


# weapon classes, inheriting from Weapon base class 

class Sword(Weapon): # done
	def __init__(self, info):
		info.update({'type':'sword'})
		super().__init__(info)

		try: self.dual_wield = info['dual_wield']
		except KeyError: self.dual_wield = False

class Bow(Weapon):
	pass

class Axe(Weapon):
	pass

class Knife(Weapon):
	pass

class Hammer(Weapon):
	pass






# Stack class, to make stacks of items

class Stack:
	STACK_LIMIT = 32
	def __init__(self, item, amount=1):
		self.name = item.name
		self.item = item
		self.amount = amount 

	@property
	def isempty(self):
		return not bool(self.amount)

	@property
	def isfull(self):
		return not bool(self.isempty)

	def get(self, amount=1): # get item object, and remove amount

		""" warning: changing item's properties changes the properties of items in the stack,
		so its better to make the stackability of the object False if you plan to change its
		properties """

		self.remove(amount)
		return self.item 

	def add(self, amount=1): # increment stack amount and return remainder, used with player.add_to_stack
		remainder = amount - (self.STACK_LIMIT - self.amount) 
		if remainder <= 0:
			self.increment(amount)
			remainder = 0
		else:
			self.increment(amount-remainder)
		return remainder

	def remove(self, amount=1):
		remainder = self.amount - amount # left to subtract
		
		if remainder <= 0:
			self.decrement(amount)
			remainder = -remainder
		else:
			self.decrement(amount)
			remainder = 0

		return remainder


	def increment(self, amount=1):
		if self.item.stackable:
			self.amount += amount
			if self.amount > Stack.STACK_LIMIT:
				self.amount = Stack.STACK_LIMIT
				return False # full
			return True # space left
		else:
			return None # not stackable

	def decrement(self, amount=1):
		if self.item.stackable:
			self.amount -= amount
			if self.amount < 0:
				self.amount = 0
				return False # empty
			return True # not empty yet
		else:
			return None # not stackable

	def reset(self):
		self.amount = 0



# dictionaries for defining certain class attributes

"""
weapon = Weapon({
			'name':'sword',
			'durability':100,
			'damage':24,
			'slot':'forehand',
			'rarity':'rare',
			'wear_down':5,
			'type':'sword',
			'recipe':'recipe',
			'req_stats':None,
			'req_lvls':None
		})
"""
