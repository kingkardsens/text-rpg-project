# REQUIRES: 13,20,rpgutility

import pickle
from test_20 import Location
from test_13 import Menu
from rpgutility import settings

import random
import copy

divider = settings['divider']

class Room:
	def __init__(self, name, function, lines=[]):
		self.name = name
		self.function = function
		self.lines = lines

	def enter(self,player=None):
		try:
			self.function(self,player)
		except TypeError:
			self.function(self)

class Environment:
	def __init__(self, name, room_list, lines=[],enterfunc=None):
		self.name = name
		self.room_list = room_list
		self.enterfunc = enterfunc
		self.lines = lines


	def enter(self,player=None):
		player.location = self
		if self.enterfunc:
			try:
				if player: val = self.enterfunc(self,player)
				else: val = self.enterfunc(self)
			except TypeError: val = self.enterfunc(self)
			return val
		else:
			end = False
			while True:
				n=1
				print('-----------------')
				print(self.name)
				print('-----------------')
				for room in self.room_list:
					print(f'[{n}] {room.name}')
					n+=1
				print('[q] move on')
				print('[e] exit')
				print('-----------------')
				roomnum = input('> ').strip()
				Menu.clean()
				try:
					try:
						roomnum = int(roomnum)
					except ValueError:
						if roomnum == 'q':
							break
						if roomnum == 'e':
							end = True
							break
						else:
							print('option should be a number')
							continue
					room = self.room_list[roomnum-1]
				except IndexError:
					print('option doesnt exist')
					continue
				try:
					if self.player: room.enter(self.player)
					else: room.enter()
				except: room.enter()
					
			if end == True: return True # return true if exiting location
				

class Levels:
    def __init__(self,name,xp,level):
        self.name = name
        self.xp = xp
        self.level = level
        self.required_xp = {1:100, 2:130, 3:140, 4:160, 5:200} # to level up

    def update(self,player):
        required_xp = self.required_xp[self.level]
        if player.checklevels(self.name,self.level,required_xp):    
            if self.level+1 in self.required_xp.keys():
                self.level += 1
                self.xp = 0
            
    def add(self,xp,player):
        self.xp += xp
        self.update(player)

class Inventory:
    def __init__(self):
        self.items = {}
        self.weapons = []
class Bank:
    def __init__(self):
        self.items = {}
        self.weapons = []
        self.gold = 0

class Player:
	def __init__(self,name,gold,location=None,env_list=[],seed=1):
		self.name = name 
		self.hp = 200
		self.mhp = 200 
		self.mp = 250
		self.mmp = 250
		self.xp = 0
		self.level = 1
		self.gold = gold 
		self.location = location 
		self.coords = Location(env_list,seed)
		self.environments = env_list
		# slots
		self.slots={'forehand':None,'offhand':None,'armor':None,'dual_wield':False}
		#combat related
		self.levellist = {}
		self.initialiselevels()
		self.statuseffect = None
		self.attack = 10
		self.defense = 10
		self.engaged = None
		self.stamina = 100
		self.total_stamina = 100
		self.combat_options = []
		self.attack_counter = 0
		# inventory and bank
		self.inventory = Inventory()
		self.bank = Bank()
		# stat points
		self.dex = 0
		self.int = 0
		self.str = 0
		self.vit = 0
		self.stat_points = 10
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

	def addxp(self,level,xp):
		self.levellist[level].add(xp,self)

	def deductmoney(self,amount):
		self.gold -= amount
		if self.gold < 0: self.gold = 0

	def addmoney(self,amount):
		self.gold += amount

	def buyitem(self,item,amount=1,weapon=False):
		self.deductmoney(item.cost*amount)
		self.giveitem(item,weapon)

	def heal(self,amount):
		self.hp += amount

	def damage(self,amount):
		self.hp -= amount
		if self.hp < 0: self.hp = 0

	def setstatuseffect(self,statuseffect):
		self.statuseffect = statuseffect

	def removestatuseffect(self):
		self.status = None

	def clearinventory(self,items=True,weapons=True):
		if items:
			self.inventory.items = {}
		if weapons:
			self.inventory.weapons = []

	def executeaffect(self,statuseffect):
		if statuseffect:
			statuseffect.affect(self)

	def getslotitembuffs(self):
		attack,defence = 0,0
		for slot in self.slots.keys():
			if self.slots[slot]:
				item = self.slots[slot]
				try:
					defence += item.defence
				except AttributeError:
					pass
				try:
					attack += item.attack
					if item.dual_wield==True and slot == 'offhand':
						attack -= item.attack
					
				except AttributeError:
					pass
		return [attack,defence]

	def ifabovemaxlimitcorrect(self):
		if self.hp > self.mhp: self.hp = self.mhp
		if self.mp > self.mmp: self.mp = self.mmp
		if self.stamina > self.total_stamina: self.stamina = self.total_stamina

	def equip(self,index):
		item = self.inventory.weapons[index]
	
		
		for slotname in self.slots.keys():
			if item.slot == slotname:
				if self.slots[slotname]:
					self.unequip(self.slots[slotname].name)
				self.slots[slotname] = item				

		try:
			if item.dual_wield:
				if self.slots['offhand']:
					item2 = self.slots['offhand']
					self.giveitem(item2,weapon=True)
					self.unequip(self.slots['offhand'].name)	
				self.slots['offhand'] = item
				self.slots['dual_wield'] = True

		except AttributeError: pass
		self.removeitem(index)

	def boostfromslots(self):
		pass

	def unequip(self,itemname,slot=None): # add slotlist to player to contain self.offhand, etc.

		if not slot:
			for slot in list(self.slots.keys())[:2]: # because last item is a bool 'dual_wield'
				if self.slots[slot]:
					if itemname == self.slots[slot].name:
						item = self.slots[slot]
						self.giveitem(item,weapon=True)
						self.slots[slot] = None
					break
		else:

			item = self.slots[slot]
			self.giveitem(item,weapon=True) 
			self.slots[slot] = None

		try:
			if item.dual_wield:
				self.slots['offhand'] = None
				self.slots['dual_wield'] = False
		except AttributeError: pass
			

	def maxstats(self):
		self.stamina = self.total_stamina
		self.hp = self.mhp
		self.mp = self.mmp
		self.engaged = None
		self.attack_counter = 0



	def resetstats(self):
		for stat in self.__dict__:
			if type(self.__dict__[stat]) is list:
				self.__dict__[stat] = []
			elif type(self.__dict__[stat]) is dict:
				self.__dict__[stat] = {}
			elif type(self.__dict__[stat]) is int:
				self.__dict__[stat] = 0
			else:
				self.__dict__[stat] = None

	def inviteminstance(self,itemname):
		for inventoryitem in self.inventory.items:
			if itemname == inventoryitem.name:
				return inventoryitem		
		return None

	def weaponinstance(self,index):
		weapons = self.inventory.weapons
		try:
			weapon = weapons[index]
			return weapon
		except AttributeError:
			return None

	def giveitem(self,item,amount=1,weapon=False):
		if not weapon:
			if not item.stackable:
				self.inventory.items[item] = 1
			elif self.checkitem(item):
				self.inventory.items[self.inviteminstance(item.name)] += amount
			else:
				self.inventory.items[item] = amount
		else:
			weapon = item
			self.inventory.weapons.append(weapon)


	def removeitem(self,itemname,amount=1):
		try:
			index = int(itemname)
			weapon = self.weaponinstance(index)
			self.inventory.weapons.remove(weapon)
		except ValueError:
			item = self.inviteminstance(itemname)
			if not item:
				return False
			else:
				if amount >= self.inventory.items[item]:
					del self.inventory.items[item]
				else:
					self.inventory.items[item] -= amount
		
	def levelsrequirement(self,req_dict):
		for requirement in req_dict.keys():
			if not self.checklevels(requirement,req_dict[requirement]):
				return False
		return True

	def checkitem(self,item,amount=1):
		try:
			name = item.name
		except AttributeError:
			name = item


		if not bool(self.inventory.items):
			return False
		for inventoryitem in self.inventory.items:
			if name == inventoryitem.name:
				if self.inventory.items[inventoryitem] >= amount:
					return True
				else:
					return False
		for weapon in self.inventory.weapons:
			if name == weapon.name:
				return True
			else:
				return False
		
		return False

	def checklevels(self,levelname,levelreq,xpreq=0):
		for levels in self.levellist.keys():
			if levelname == levels:
				if self.levellist[levels].level >= levelreq and self.levellist[levels].xp >= xpreq:				
					return True
				else:
					return False
		return True

	def checkplayerlevel(self,reqlevel):
		if self.player.level >= reqlevel:
			return True
		else:
			return False

	def checkstats(self,stats_dict):
		for stat in stats_dict.keys():
			if self.__dict__[stat] < stats_dict[stat]:
				return False
		return True

	def satisfyitemreq(self,item):
		if 'req' not in item.__dict__.keys() and 'levels_req' not in item.__dict__.keys():
			return None

		if item.__dict__['req']:
			if not self.checkstats(item.req):			
				return False

		if item.__dict__['levels_req']:
			for levels in item.levels_req.keys():
				if not self.checklevels(levels,levels_req[levels]):
					return False

		

		return True


	def setstats(self,stat_dict):
		player_stats = self.__dict__
		for type_ in stat_dict.keys():		 
			for criteria in stat_dict[type_]: 				 
				if criteria in player_stats.keys():					
					if type_ == 'buff':
						player_stats[criteria] += stat_dict[type_][criteria]
					elif type_ == 'nerf':
						player_stats[criteria] -= stat_dict[type_][criteria]
						if player_stats[criteria] < 0: player_stats[criteria] = 0
					elif type_ == 'set':
						player_stats[criteria] = stat_dict[type_][criteria]
					elif type_ == 'mult':
						player_stats[criteria] *= stat_dict[type_][criteria]
						if int(player_stats[criteria]) < 0: player_stats[criteria] = 0
		self.ifabovemaxlimitcorrect()

	def use(self,item,*args):
		if self.checkitem(item):
			try:
				value = item.use(self,args)
			except TypeError:
				value = item.use(self)
			return value
		else:
			return None

	def execute_skill(self,skill,entity=None):
		try:
			if entity:
				skill.execute(self,entity)
			else:
				print('entity was not specified in execute_skill')
			
		except TypeError:
			skill.execute(self)

	def assignstatpoints(self,stat,point=1):
		if stat == 'dex': self.dex += point
		elif stat == 'vit': self.vit += point
		elif stat == 'str': self.str += point
		elif stat == 'int': self.int += point

	def die(self):
		self.gold = 0
		self.location = 'town'
		for levels in self.levellist.values():
			levels.xp=0
		self.maxstats()

	def displaystats(self):
		print(divider)
		print(' '*42+'STATS')
		print(divider)
		print(f'Name: {self.name.upper()}')
		print(f'{self.hp}/{self.mhp} HP')
		print(f'{self.mp}/{self.mmp} MP')
		print(f'Level: lvl {self.level}, {self.xp} XP')
		print(f'Gold: {self.gold}')
		print(f'Location: {self.location.name}')
		print(divider)
		print('GEAR')
		print(divider)
		for slot in list(self.slots.keys())[:3]:
			if self.slots[slot]:
				print(f'{slot}: {self.slots[slot].name}')
			else:
				print(f'{slot}: {None}')
		print(divider)


	def save(self,filename='rpgsavefile'):
		with open(filename+'.sav','wb') as f:
			pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)

	def load(self,filename='rpgsavefile'):
		with open(filename+'.sav','rb') as f:
			load_game = pickle.load(f)
		self.__dict__.update(load_game)


class Game:
	def __init__(self,name,gold,seed=0,env_list=[],location=None):
		self.seed = seed
		self.player = Player(name,gold,seed=seed,env_list=env_list,location=location)








			
			
		

# beyond this is untested territory - be careful



class Entity:
	def __init__(self,name,hp,mp,attack,defense,attack_pattern,golddrop=100,xpdrop=10,whichlevels=['combat'],spawn_env=[],drops={},function=None):
		self.name = name 
		self.hp = hp
		self.mhp = hp
		self.mp = mp
		self.mmp = mp
		self.spawn_env = spawn_env
		self.function = function
		
		#combat related
		self.attack_pattern = attack_pattern
		self.current_attack_index = 0
		self.statuseffect = None
		self.attack = attack
		self.defense = defense
		self.stamina = 100
		self.total_stamina = 100
		
		self.drops = drops
		self.xpdrop = xpdrop
		self.golddrop = golddrop
		self.whichlevels = whichlevels

	def damage(self,amount):
		self.hp -= amount
		if self.hp < 0:
			self.hp = 0

	def heal(self,amount):
		self.hp += amount
		if self.hp > self.mhp:
			self.hp = self.mhp

	def setstatuseffect(self,statuseffect):
		self.statuseffect = statuseffect

	def removestatuseffect(self):
		self.statuseffect = None

	def executeaffect(self,statuseffect):
		if statuseffect:
			statuseffect.affect(self)

	def execute_skill(self,skill,entity=None):
		try:
			if entity:
				skill.execute(self,entity)
			else:
				print('entity was not specified in execute_skill')
			
		except TypeError:
			skill.execute(self)

	def ifabovemaxlimitcorrect(self):
		if self.hp > self.mhp: self.hp = self.mhp
		if self.mp > self.mmp: self.mp = self.mmp
		if self.stamina > self.total_stamina: self.stamina = self.total_stamina

	def setstats(self,stat_dict):
		entity_stats = self.__dict__
		for type_ in stat_dict.keys():		 
			for criteria in stat_dict[type_]: 				 
				if criteria in entity_stats.keys():					
					if type_ == 'buff':
						entity_stats[criteria] += stat_dict[type_][criteria]
					elif type_ == 'nerf':
						entity_stats[criteria] -= stat_dict[type_][criteria]
						if player_stats[criteria] < 0: entity_stats[criteria] = 0
					elif type_ == 'set':
						entity_stats[criteria] = stat_dict[type_][criteria]
					elif type_ == 'mult':
						entity_stats[criteria] *= stat_dict[type_][criteria]
						if int(entity_stats[criteria]) < 0: entity_stats[criteria] = 0
		self.ifabovemaxlimitcorrect()

	def returndrops(self):
		drop = random.choice(list(self.drops.keys()))
		return drop

	def returnmultipledrops(self,amount):
		drops = []
		for i in range(amount):
			drops.append(self.returndrops())
		return drops

	def checkstats(self,stats_dict):
		for stat in stats_dict.keys():
			if self.__dict__[stat] < stats_dict[stat]:
				return False
		return True

	def entitydiereset(self):
		self.hp = self.mhp
		self.mp = self.mmp
		self.stamina = self.total_stamina 
		self.removestatuseffect() 
		self.current_attack_index = 0



class Battle:
	def __init__(self,player,entity):
		self.player = player
		self.player_lines = 'You assume a fight stance'
		self.entity = entity
		self.entity_lines = 'The '+entity.name.upper()+' stands ready to strike'
		self.turn_count = 0

		self.combo_list = []
		self.temp_combat_options = []

		# used for entity attack options
		self.combonum = 0
		self.atknum = 0

		

		

	def print_bar(self,entity,stats,char='█',empty='░',join=False,s='|',l='|'):

		stat1 = entity.__dict__[stats[0]]
		stat2 = entity.__dict__[stats[1]]
		
		join_var = ' '
		print(s+char*int((int(stat1)/10))+empty*int((int(stat2)-int(stat1))/10)+l,stat1,'/',stat2,end=join_var)
		if not join:
			print()


	def display(self):
		print()
		for current_entity in [self.entity,self.player]:
			if current_entity is self.entity:
				print('>',self.entity_lines)
			else:
				print('>',self.player_lines)
			print()
			print('   '+current_entity.name.upper())
			print()
			self.print_bar(current_entity,['hp','mhp'],join=True)
			try:
				print('HP  EFFECT: [',current_entity.statuseffect.name,']')
			except AttributeError:
				print('HP  EFFECT: [',current_entity.statuseffect,']')
			print()
			print('          ',end='')
			self.print_bar(current_entity,['mp','mmp'],join=True)
			print('MP')
			print()

		
		print('          ',end='')
		self.print_bar(self.player,['stamina','total_stamina'],join=True,char='□',empty=' ',s='[',l=']')
		print('STAMINA',f' <<{self.turn_count}>>')
		print()
		print('---------------------------------------------------------------')
		print()
		


	def choose_attack_combos(self):
		combat_options = []
		if len(self.temp_combat_options) < 4:
			temp = copy.deepcopy(self.player.combat_options)
		else:
			temp = self.temp_combat_options
		
		for i in range(0,4):
			attack_combo = random.choice(temp)

			temp.remove(attack_combo)
			combat_options.append(attack_combo)


		self.combo_list = combat_options
		self.temp_combat_options = temp
		

	def print_attack_combo(self,attack_combo):
		print(' -',end=' ')
		for attack in attack_combo:
			print(attack.name,end=', ')
		print()

	def display_attacks(self):
		n = 1
		for attack_combo in self.combo_list:
			try:
				print(n,attack_combo[0].name,end=' ')

				if len(attack_combo) == 3:
					print('starter')
				elif len(attack_combo) == 2:
					print('linker')
				elif len(attack_combo) == 1:
					print('finisher')
			except IndexError:
				print(n,'empty')
			n+=1


	def check_if_combo_empty(self,index):
		if not bool(self.combo_list[index]):
			return True
		if len(self.combo_list[index]) <= 0:
			return True
		else:
			return False

	def check_if_all_empty(self):
		n = 0
		if not bool(self.combo_list):
			return True
		for attack_combo in self.combo_list:
			if not self.check_if_combo_empty(n):
				return False
			n+=1
		return True
			
	def effect_dealt(self,entity_skill,whoattack):
		playername = self.player.name
		entityname = self.entity.name
		damage = 0
		heal = 0
		effect = None
		dealt = ''
		if whoattack == 'player':
			damage += self.player.getslotitembuffs()[0]
			heal += self.player.getslotitembuffs()[1]
					
		try: damage += entity_skill.damage			
		except AttributeError: pass			
		try: heal += entity_skill.heal_val			
		except AttributeError: pass
		try: effect = entity_skill.effect
		except AttributeError: pass
		
		who = None
		if entity_skill.whoeffect == 'player':
			if whoattack != 'entity': who = playername
			else: who = entityname
		elif entity_skill.whoeffect == 'entity':
			if whoattack != 'entity': who = entityname			
			else: who = playername

		if whoattack != 'entity':
			if self.player.stamina > 0:
				damage = damage+self.player.attack+self.player.str*2-self.entity.defense
				if damage != 0: dealt += ' dealt '+str(damage)+' damage to '+who+','			
			else:
				dealt = 'couldnt attack, low stamina'
				return dealt
		else:
			damage = damage+self.entity.attack-self.player.defense
			if damage != 0: dealt += ' dealt '+str(damage)+' damage to '+who+','
		
		if heal != 0: dealt += ' healed '++"'s "+str(heal)+' HP,'			
		if effect: dealt += ' affected '+who+' with '+entity_skill.effect.name
			
		return dealt

		'''
		other = ''
		try:
			a = entity_skill.increase_stat
			other += ' and increased '+entity_skill.whoeffect+"'s"+' stats!'
		except AttributeError:
			pass
		try:
			a = entity_skill.decrease_stat
			other += ' and decreased '+entity_skill.whoeffect+"'s"+' stats!'
		except AttributeError:
			pass
		'''

	def entity_attack(self):
		try: entity_skill = self.entity.attack_pattern[self.entity.current_attack_index]
		except AttributeError:
			entity_skill = self.entity.combat_options[self.combonum][self.atknum]
			self.atknum+=1
			if self.atknum == 2:
				self.combonum+=1
				if self.combonum >= len(self.entity.combat_options):
					self.combonum = 0
				self.atknum = 0

		self.entity.execute_skill(entity_skill,self.player)
		try:
			self.entity.current_attack_index += 1
			if self.entity.current_attack_index >= len(self.entity.attack_pattern):
				self.entity.current_attack_index = 0
		except AttributeError: pass

		dealt = self.effect_dealt(entity_skill,'entity')
		self.entity_lines = self.entity.name.upper()+' '+dealt+' with '+entity_skill.name.upper()

	def check_death(self,entity):
		if entity.hp <= 0:
			return True
		return False

	def print_drops(self,drop,amount):
		print('     you killed the '+self.entity.name.upper()+' and recieved a drop!')
		print('      [',drop.name,' x',amount,']')
		print('      xp:',self.entity.xpdrop)
		print('      gold:',self.entity.golddrop)
		print()

	def start_battle(self):
	
		alive = True
		# keep battling while either of the 2 are alive i.e. alive = True
		while alive:
			# choose random 4 attack combos from player.combat_options
			if self.check_if_all_empty(): self.choose_attack_combos()
	
			# execute status effect affects on both entities
			self.player.executeaffect(self.player.statuseffect)
			self.entity.executeaffect(self.entity.statuseffect)

			# display hp bars and other bars, display chosen attack combos, turn count increment by 1
			self.display()
			self.display_attacks()
			self.turn_count+=1

			# ask for attack choice only if both are alive, else set alive = False
			if not self.check_death(self.player) and not self.check_death(self.entity):
				choice = int(input('> '))

				try:
					# check if the specified attack's combo list is empty, if not then attack entity, change player lines, remove attack from combo list
					if not self.check_if_combo_empty(choice-1):
						player_skill = self.combo_list[choice-1][0]
						self.player.execute_skill(player_skill,self.entity)
						if self.player.stamina > 0:
							self.combo_list[choice-1].pop(0)
							#if self.check_if_combo_empty(choice-1): 
						dealt = self.effect_dealt(player_skill,'player')
						self.player_lines = self.player.name.upper()+' '+dealt+' with '+player_skill.name.upper()

					else: 
						# if combo is empty still make entity attack
						self.entity_attack()
						continue
				except IndexError:
					print('no such choice')

				# entity attacks regardless of what player does
				self.entity_attack()
			else:
				# if either of the 2 are dead set alive to False
				# change player lines and entity lines for the 2 death scenario lines

				if self.check_death(self.player):
					self.entity_lines = self.entity.name.upper()+' killed '+self.player.name
					self.player_lines = 'You are dead'
				elif self.check_death(self.entity):
					self.player_lines = self.player.name.upper()+' killed the '+self.entity.name
					self.entity_lines = self.entity.name.upper()+' was killed by '+self.player.name
				alive = False

		# display player_lines, attack_lines and hp bars
		self.display()

		# if player dies max hp and stamina while resetting params like gold and xp
		if self.check_death(self.player):
			self.player.die()
			self.player.maxstats()
			self.entity.entitydiereset()
			print()
			pause = input('press enter to continue...')

		# if entity dies dont heal player, give drops, add xp, add gold, display drops and reset entity for another battle
		elif self.check_death(self.entity):
			for level in self.entity.whichlevels:
				self.player.addxp(level,self.entity.xpdrop)
			self.player.addmoney(self.entity.golddrop)
			self.entity.entitydiereset()

			drop = self.entity.returndrops()
			amount = self.entity.drops[drop]

			if not drop.stackable: amount = 1
				
			self.player.giveitem(drop,amount)
			self.print_drops(drop,amount)
			pause = input('press enter to continue...')

		
			





		


			
			
		
		
		

