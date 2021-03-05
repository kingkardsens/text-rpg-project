from test_18 import Player,Dummy,Skill,skill_tree,villagerooms
from test_20 import Location
from colorama import Fore, Style
import colorama
from test_13 import Menu
colorama.init()


# looting dungeoneering combat stuff like that
s1 = Dummy(12,0,'s1')
s2 = Dummy(14,0,'s2')
s3 = Dummy(8,0,'s3')

player = Player([s1,s2,s3])














class Item:
	def __init__(self, name, info, function, cost=False, sell_cost=False):
		self.name = name
		self.info = info
		self.function = function
		self.cost = cost
		self.sell_cost = sell_cost
		self.stackable = True

	def use(self, player, args):
		try:
			value = self.function(player,args)
		except TypeError:
			value = self.function(player)
		return value

	


class Food(Item):
	def __init__(self, name, info, heal_val, cost=False, sell_cost=False):
		super().__init__(name, info, None, cost, sell_cost)
		self.heal_val = heal_val

	def use(self, player):
		player.affect = 'bread'
	   #player.hp += self.heal_val

class Magic(Item):
	def __init__(self, name, info, stat_dict, cost=False, sell_cost=False): # buff, nerf, set, mult
		super().__init__(name, info, None, cost, sell_cost)
		self.stat_dict = stat_dict
		

	def use(self, player):
		player_stats = player.__dict__
		for type_ in self.stat_dict.keys():		 # {'buff':{},'nerf':{},'set':{}}
			for criteria in self.stat_dict[type_]: 				 
				if criteria in player_stats.keys():					
					if type_ == 'buff':
						player_stats[criteria] += self.stat_dict[type_][criteria]
					elif type_ == 'nerf':
						player_stats[criteria] -= self.stat_dict[type_][criteria]
					elif type_ == 'set':
						player_stats[criteria] = self.stat_dict[type_][criteria]
					elif type_ == 'mult':
						player_stats[criteria] *= self.stat_dict[type_][criteria]

class Weapon(Item):
	def __init__(self, info_dict):
		super().__init__(info_dict['name'], info_dict['info'], None, info_dict['cost'], info_dict['sellcost'])
		self.rarity = info_dict['rarity']
		self.slot = info_dict['slot']
		self.durability = info_dict['durability']
		self.max_durability = info_dict['maxdur']
		self.attack = info_dict['attack']
		self.effect = info_dict['effect']
		self.wear_down = info_dict['wear_down']
		self.type = info_dict['type']
		self.recipe = info_dict['recipe']
		self.req = {'wield_level':info_dict['wield_level'],'smith_level':info_dict['smith_level']}
		self.stackable = False
		self.info_dict = info_dict

# info_dict['name'],info_dict['cost'],info_dict['sellcost'],info_dict['rarity'],info_dict['slot'], info_dict['durability'], info_dict['maxdur'], info_dict['attack'], info_dict['effect'],info_dict['info'], info_dict['wear_down'],info_dict['recipe'],info_dict['wield_level'],info_dict['smith_level']

class Sword(Weapon):
	def __init__(self, info_dict, dual_wield=False):
		super().__init__(info_dict)
		self.dual_wield = dual_wield





sword_base = {
	'name':'sword',
	'cost':10,
	'sellcost':10,
	'rarity':'common',
	'tag':'sword',
	'slot':'forehand',
	'durability':'100',
	'maxdur':'100',
	'attack':20,
	'effect':None,
	'info':'a common sword',
	'wear_down':5,
	'type':'sword',
	'recipe':{'material variable':'material amount'},
	'wield_level':0,
	'smith_level':0
					}




sword = Sword(sword_base)




class Environment:
	def __init__(self, name, room_list):
		self.name = name
		self.room_list = room_list

	def enter(self):

		while True:
			n=1
			print('-----------------')
			print(self.name)
			print('-----------------')
			for room in self.room_list:
				print(f'[{n}] {room.name}')
				n+=1
			print(f'[{n}] Exit')
			print('-----------------')
			try:
				try:
					roomnum = int(input('> '))
				except ValueError:
					print('option should be a number')
					continue
				if roomnum == n:
					quit()

				room = self.room_list[roomnum-1]
			except IndexError:
				print('option doesnt exist')
				continue
			room.enter()



village = Environment('village',villagerooms)
#village.enter()









coords = Location([
					Fore.YELLOW+'village'+Style.RESET_ALL,
					Fore.BLUE+'plains '+Style.RESET_ALL,
					Fore.GREEN+'forest '+Style.RESET_ALL,
					Fore.BLUE+'plains '+Style.RESET_ALL,
					Fore.GREEN+'forest '+Style.RESET_ALL,
					Fore.BLUE+'plains '+Style.RESET_ALL,
					Fore.GREEN+'forest '+Style.RESET_ALL,
					Fore.BLUE+'plains '+Style.RESET_ALL,
					Fore.GREEN+'forest '+Style.RESET_ALL],9,[0,0])
#coords.move('up',2)
#coords.display()
#print(coords.generate())


def move_sequence(direction):
	direction = direction[0]
	coords.move(direction)
	coords.display()
	print('-'*90)
	print()
	coords.surroundings(7,True)

a = Menu({
			'title':'MOVE TEST',
			'options':{
						'up':[move_sequence,('up',None),'w'],
						'down':[move_sequence,('down',None),'s'],
						'right':[move_sequence,('right',None),'d'],
						'left':[move_sequence,('left',None),'a'],
						'Exit':[quit,'e']   
						}
							})

a.runMenu(end=False)






































# bread = Food('bread','hunger up',12)
# crystal = Magic('crystal','buff health',{'set':{'affect':'CRYSTAL'}})
# skill_tree['combat']['fire'].execute(player)

#print(sword.info)

#print(player.affect)
#player.execute_skill(skill_tree['combat']['fire'])
#print(player.affect)















'''

info_dict = {
	'name':'',
	'cost':'',
	'sellcost':'',
	'rarity':'',
	'tag':'',
	'slot':'',
	'durability':'',
	'maxdur':'',
	'attack':'',
	'defense':'',
	'effect':'',
	'info':'',
	'wear_down':'',
	'type':'',
	'recipe':'',
	'wield_level':'',
	'smith_level':''
					}
'''