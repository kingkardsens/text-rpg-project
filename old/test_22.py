class Item:
	def __init__(self, name, info, function, cost=False, sell_cost=False,stackable=True):
		self.name = name
		self.info = info
		self.function = function
		self.cost = cost
		self.sell_cost = sell_cost
		self.stackable = stackable

	def use(self, player, *args):
		if self.function:
			try:
				value = self.function(player,args)
			except TypeError:
				value = self.function(player)
			return value
		else:
			print('you cant use this object')
			return False

		

	


class Food(Item):
	def __init__(self, name, heal_val, info=None, cost=False, sell_cost=False,stackable=True):
		super().__init__(name, info, None, cost, sell_cost,stackable)
		self.heal_val = heal_val

	def use(self, player):
		player.hp += self.heal_val
		if player.hp > player.mhp:
			player.hp = player.mhp
		player.removeitem(self.name)

class Magic(Item):
	def __init__(self, name,stat_dict,info=None, req=None,levels_req=None,onetimeuse=False,cost=False, sell_cost=False,stackable=False): # buff, nerf, set, mult
		super().__init__(name, info, None, cost, sell_cost,stackable)
		self.stat_dict = stat_dict
		self.onetimeuse = onetimeuse
		self.req = req
		self.levels_req = levels_req
		

	def use(self, player):
		if player.satisfyitemreq(self) != False:
			player.setstats(self.stat_dict)
			if self.onetimeuse:
				player.removeitem(self.name)
		else:
			print('you cant use this yet')
			return False

class Weapon(Item):
	def __init__(self, info_dict):
		super().__init__(info_dict['name'], info_dict['info'], None, info_dict['cost'], info_dict['sellcost'],False)
		self.rarity = info_dict['rarity']
		self.slot = info_dict['slot']
		self.durability = info_dict['durability']
		self.max_durability = info_dict['maxdur']
		self.attack = info_dict['attack']
		self.effect = info_dict['effect']
		self.wear_down = info_dict['wear_down']
		self.type = info_dict['type']
		self.recipe = info_dict['recipe']
		self.levels_req = {'smithing':info_dict['smith_level']}
		self.req = {'level':info_dict['wield_level']}

		try:
			if info_dict['levels_req']:
				self.levels_req.update(info_dict['levels_req'])
		except:
			pass
		
		try:
			if info_dict['req']:
				self.req.update(info_dict['req'])
		except:
			pass

		self.info_dict = info_dict

class Material(Item):
	def __init__(self,name,info=None,req_smithlevel=0,cost=False,sell_cost=False):
		super().__init__(name,info,None,cost,sell_cost)
		self.levels_req = {'smithing':req_smithlevel}

# info_dict['name'],info_dict['cost'],info_dict['sellcost'],info_dict['rarity'],info_dict['slot'], info_dict['durability'], info_dict['maxdur'], info_dict['attack'], info_dict['effect'],info_dict['info'], info_dict['wear_down'],info_dict['recipe'],info_dict['wield_level'],info_dict['smith_level']

class Sword(Weapon):
	def __init__(self, info_dict, dual_wield=False):
		super().__init__(info_dict)
		self.dual_wield = dual_wield


class Statuseffect:
	def __init__(self,name,stat_dict,repititive=True,repeat_times=0,function=None):
		self.name = name
		self.stat_dict = stat_dict
		self.repititive = repititive
		self.repeat_times = repeat_times+1
		self.repeat_counter = 0
		self.function = function

	def affect(self,entity):
		self.repeat_counter += 1
		if self.repeat_counter >= self.repeat_times:
			self.repeat_counter = 0
			entity.statuseffect = None
		else:
			if self.function:
				self.function(entity)
			else:
				entity.setstats(self.stat_dict)



class Skill:
	def __init__(self,name,info,req,levels_req,run,effect,whoeffect):
		self.name = name
		self.info = info
		self.req = req 
		self.levels_req = levels_req    # requirements -- 
		self.run = run 
		self.effect = effect
		self.whoeffect = whoeffect


	def execute(self,player,entity):
		if self.satisfyitemreq(skill):
			self.run(player,entity)			
		else:
			print('You cant use this yet')

	def seteffect(self,entity):
		if self.effect:
			entity.statuseffect = self.effect

'''
	@staticmethod
	def print_skill_tree(skill_tree,branch='all'):	
		if branch != 'all':
			print('==-'*20)
			print('  [[ '+branch+' ]]')
			print('==-'*20)
			print()
			index = 0
			for skill in skill_tree[branch].keys():
				if index % 2 != 0 or index == 0:
					print('  ['+skill,end=']   ')

				else:
					print('  ['+skill+']')
					print()
					index = -1
				index+=1
			print()
			print()
			print('==-'*20)
		else:
			for branch_ in skill_tree:
				print_skill_tree(skill_tree,branch=branch_)
				print()
				print()
'''

class Attack(Skill):
	def __init__(self,name,damage,decrease_stat=None,req=None,levels_req=None,info=None,effect=None,whoeffect='entity'):
		super().__init__(name,info,req,levels_req,None,effect,whoeffect)
		self.damage = damage
		self.decrease_stat = decrease_stat # {'stamina':23} decrease stamina by 23
		
		

	def execute(self,player,entity):
		try:
			if player.satisfyitemreq(self):
				pass
			else:
				print('cant use this attack')
				return None
		except AttributeError:
			pass
		try:
			if player.stamina > 0:
				entity.damage((self.damage+player.attack+player.str*2+player.getslotitembuffs()[0])-entity.defense)
		except AttributeError:
			entity.damage((self.damage+player.attack)-entity.defense)
			
		
		
		
		if self.decrease_stat: player.setstats({'nerf':self.decrease_stat})			

		if self.whoeffect == 'entity': self.seteffect(entity)
		else: self.seteffect(player)
			




class Heal(Skill):
	def __init__(self,name,heal_amount,increase_stat=None,req=None,levels_req=None,info=None,effect=None,whoeffect='player'):
		super().__init__(name,info,req,levels_req,None,effect,whoeffect)
		self.heal_val = heal_amount
		self.increase_stat = increase_stat
		

	def execute(self,player): # we dont really need entity
		try:
			if not player.satisfyitemreq(self):
				print('cant use this skill')
				return None
		except AttributeError: pass
		
		

		player.heal(self.heal_val)
		
		if self.increase_stat: player.setstats({'buff':self.increase_stat})
		if self.whoeffect == 'entity': self.seteffect(entity)
		else: self.seteffect(player)
