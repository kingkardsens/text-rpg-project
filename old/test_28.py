# REQUIRES: 13,21,27,rpgutility

from test_13 import Menu
from test_21 import Game
import test_27 
from rpgutility import getcfile, writetoconfig,save_extension,config_file,settings

#from test_22 import Item, Food, Magic, Weapon, Sword, Statuseffect, Attack, Heal, Skill
#from test_21 import Room, Environment, Levels, Inventory, Bank, Player, Game, Entity, Battle
# Loki_the_Great#3131

import random
import os


random_map = settings['playerdefined']['random_map']
version = settings['version']
rpgtitle = settings['title']

# main gameloop

def main_gameloop(game):
	random.seed(game.seed)
	stop = False
	stop = game.player.location.enter(game.player)
	while stop is False:
		if not random_map:
			stop = game.player.movement_handler()
		else:
			env = random.choice(game.player.environments)
			stop = env.enter(game.player)
	return True
	



# main menu stuff


def listofsaves():
	n=1
	files = []
	for file in os.listdir():
		if '.' in file:
			extension = file.split('.')[1]
			if extension == save_extension:
				files.append(file.split('.')[0])
				print(f'[{n}] {file}')
				n+=1
	return files

def main_menu():
	game = Game('',0)

	cfile = getcfile()
	
	def whatversion():
		print(version)
		return version

	def cont(): # continue from save
		tempgame = Game('',0)
		if os.path.isfile(cfile+'.'+save_extension):
			tempgame.player.load(cfile)
			return ['return',tempgame.player.__dict__]
		else:
			print('file does not exist')

	def load_game():
		Menu.clean()
		print()
		print('LOAD GAME')
		print()
		files = listofsaves()
		print('[e] exit')
		print()
		filechoice = input('> ').strip()
		
		Menu.clean()
		if filechoice != 'e':
			filechoice = int(filechoice)
			filename = files[filechoice-1]

			tempgame = Game('',0)
			tempgame.player.load(filename)

			print()
			print('LOAD GAME STATS -',filename)
			print()
			for attr in ['name','gold','level','dex','int','vit','str']:
				print(attr,':',tempgame.player.__dict__[attr])
			print()
			print('continue with this savefile?')
			print()
			answer = input('y/n: ').strip()
			Menu.clean()
			if answer == 'y':
				writetoconfig('cfile',filename)
				return ['return',tempgame.player.__dict__]
		Menu.clean()


	def new_game():
		print('NEW GAME')
		print()
		listofsaves()
		print()
		name = input('enter name > ').strip()
		print()
		answer = input('continue? y/n >').strip()
		if answer == 'y':
			seed = random.randint(0,100)
			filename = input('savefile name > ')

			village = test_27.environments['village']
			newgame = Game(name,0,seed=seed,location=village,env_list=list(test_27.environments.values()))


			if os.path.isfile(filename+'.'+save_extension):
				print()
				print('there is already a save with this file name, would you like to overwrite it?')
				print()
				answer = input('y/n > ').strip()
				if answer == 'y':
					newgame.player.save(filename)
					writetoconfig('cfile',filename)
					Menu.clean()
					return ['return',newgame.player.__dict__]
				else:
					Menu.clean()
					new_game()
			else:
				newgame.player.save(filename)
				writetoconfig('cfile',filename)
				Menu.clean()
				return ['return',newgame.player.__dict__]
		else:
			Menu.clean()

	def exitgame():
		return ['return',False] # return to loop

	menu = Menu({
		'title':rpgtitle,
		'options':{
					'new game':[new_game,'n'],
					'load game':[load_game,'a'],
					f'continue {cfile}':[cont,'c'],
					'exit':[exitgame,'e']
					
				},
		'repeat':whatversion
		})

	value = menu.runMenu(space=10,char='',end=False)
	value = value[0]

	if value:
		game.player.__dict__.update(value)
		val = main_gameloop(game)
		return val
	else:
		return False



def loop():
	game_running = True
	while game_running:
		game_running = main_menu()

	print('you exited game')




loop()











