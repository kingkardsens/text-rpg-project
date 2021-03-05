# REQUIRES: 13,21,22,rpgutility

from test_22 import Item, Food, Magic, Weapon, Material
from test_21 import Room, Environment
from test_13 import Menu
from rpgutility import getcfile, settings

# -- -- -- -- -- -- #
import colorama
from colorama import Fore, Style, Back
colorama.init()
# -- -- -- -- -- -- #

import time
import random
clean = Menu.clean



# database for items 



foods = {
	'bread':Food('bread',40),
	'cheese':Food('cheese',20),
	'beef':Food('beef',45),
	'dumplings':Food('dumplings',30),
	'noodles':Food('noodles',25),
	'pizza':Food('pizza',35),
	'pasta':Food('pasta',35),
	'porridge':Food('porridge',25),
	'tomatosoup':Food('tomato soup',20),
	'apple':Food('apple',15),
	'orange':Food('orange',10),
	'chocolate':Food('chocolate',10),
	'sandwich':Food('sandwich',45),
	'banana':Food('banana',5),
	'nutribar':Food('nutri bar',15),
	'cookedpork':Food('cooked pork',25),
	'chicken':Food('chicken',30),
	'mushroomsoup':Food('mushroom soup',30),
	'icecream':Food('ice cream',30),
	'wafers':Food('wafers',20),
	'salad':Food('salad',10),
	'ribs':Food('ribs',10)
}


divider = settings['divider']


villagelines = [" you walk around, looking at the shops and the townsfolk.",
              " there is a light breeze, the square is active in celebration",
              " a wagon stands at the gate with goods. Old and young stand near it",
              " the people have begun to come out of the houses, chickens roam the paved streets",
              " There is a festival in town! A circus is setting up its props and tents",
              " the shops look inviting..",
              " The town looks beautiful, little children run around playing and laughing",
              " farmers are sowing the fields and its really hot, the cool bar looks inviting",
              " there is a performance! The people are crowded around a magician",
              " People are laughing and drinking at the table outside the bar, there is pleasant music"]
innlines = []
shoplines = []

def inn(player):
	print('inn')
	print('-------------------')
	

def shops(player):
	print('shops')
	print('-------------------')

def villagefunc(village,player):
	print()
	print(Fore.YELLOW+' You entered a '+village.name+Style.RESET_ALL)
	print()
	print()
	print(random.choice(villagelines))
	print()
	print(random.choice(villagelines))
	print()
	while True: # we use a while loop so that there is no need for recursion
		print(divider)
		print('',village.name,f'Name: {player.name}  {player.hp}/{player.mhp} HP  {player.mp}/{player.mmp} MP  Gold: {player.gold}  Level: {player.level}')
		print(divider)
		print(' [1] Inn')
		print(' [2] Shops')
		print(' [3] Move on')
		print(divider)
		print(' [i] inventory')
		print(' [f] stats')
		print(divider)
		print(' [s] save game')
		print(' [e] save and exit game')
		print(divider)
		choice = input(' > ').strip()
		clean()
		try:
			choice = int(choice)
			if choice <= 0: choice = 1
			if choice == 3:
				return False # to indicate we are exiting to main gameloop
			room = village.room_list[choice-1]
			room.enter(player) 
			
		except ValueError:
			if choice == 'i':
				pass
			elif choice == 'f':
				player.displaystats()
				pause = input('...')
				clean()
				
			elif choice == 's':
				player.save(getcfile())
				print('-- saved the game --')
				
			elif choice == 'e':
				player.save(getcfile())
				return True # yes stop the main gameloop
			else:
				print('no such option')
				
		except IndexError:
			print('no such option')
			





environments = {
	'village':Environment('Village',[Room(' Inn ',inn,lines=innlines), Room('Shops',shops,lines=shoplines)],lines=villagelines,enterfunc=villagefunc),
	'village2':Environment('Billage',[Room(' Inn ',inn,lines=innlines), Room('Shops',shops,lines=shoplines)],lines=villagelines,enterfunc=villagefunc),
	
}







