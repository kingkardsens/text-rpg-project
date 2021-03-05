
class Attack:
	def __init__(self, name, damage, function=None, stat_decrease={}, req_stats={}, req_lvls={}): # stat_decrease = {'hp':10}
		self.name = name
		self.damage = damage
		self.function = function
		self.stat_decrease = stat_decrease
		self.req_stats = req_stats
		self.req_lvls = req_lvls
		self.type = 'attack'

	def __call__(self, attacker, entity=None): 
		if self.stat_decrease:
			for stat in self.stat_decrease.keys():
				attacker.__dict__[stat] -= self.stat_decrease[stat]
		if self.function:
			return self.function(attacker, entity) if entity else self.function(attacker)
		else:
			if entity:
				entity.damage(self.damage)
			else:
				attacker.damage(self.damage)


class Heal:
	def __init__(self, name, amount, heal_entity=False, function=None, req_stats={}, req_lvls={}):
		self.name = name
		self.amount = amount
		self.heal_entity = heal_entity
		self.function = function
		self.req_stats = req_stats
		self.req_lvls = req_lvls
		self.type = 'heal'

	def __call__(self, healer, entity=None):
		if self.function:
			return self.function(healer, entity) if entity else self.function(healer)
		else:
			if entity and self.heal_entity:
  				entity.heal(self.amount)
			else:
  				healer.heal(self.amount)

class Spell:
	def __init__(self):
		pass


class Combo:
	def __init__(self, combo_items=[], combo_item_titles=[], req_stats={}, req_lvls={}):
		self.combo_items = combo_items
		self.combo_item_titles = combo_item_titles or ['starter', 'linker', 'finisher']
		self.current_combo_item_index = 0
		self.req_stats = req_stats
		self.req_lvls = req_lvls

	def __call__(self, user, entity):
		value = self.current_combo_item(user, entity)
		self.current_combo_item_index += 1
		if self.current_combo_item_index > len(self.combo_items)-1:
			self.current_combo_item_index = 0
		return value

	def reset(self):
		self.current_combo_item_index = 0

	@property
	def current_combo_item(self):
		return self.combo_items[self.current_combo_item_index]

	@property
	def current_item_title(self):
		return self.combo_item_titles[self.current_combo_item_index]
	



