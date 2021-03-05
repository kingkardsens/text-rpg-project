from test_13 import Menu
from test_22 import Item, Food, Magic, Weapon, Sword, Statuseffect, Attack, Heal, Skill
from test_21 import Room, Environment, Levels, Inventory, Bank, Player, Game, Entity, Battle


game = Game('Sloth',5000,'town')


punch = Attack('punch',24,decrease_stat={'stamina':10})
kick = Attack('kick',24,decrease_stat={'stamina':10}) 
tackle = Attack('tackle',24,decrease_stat={'stamina':10}) 



game.player.combat_options.append([punch,tackle,kick])
game.player.combat_options.append([tackle,kick,punch])
game.player.combat_options.append([kick,tackle,punch])


sword_base = {
				'name':'sword',
				'cost':10,
				'sellcost':10,
				'rarity':'common',
				'tag':'sword',
				'slot':'forehand',
				'durability':100,
				'maxdur':100,
				'attack':20,
				'effect':None,
				'info':'a common sword',
				'wear_down':5,
				'type':'sword',
				'recipe':{'material variable':'material amount'},
				'wield_level':0,
				'smith_level':0,
				'levels_req':None,
				'req':None
				
								}

sword = Sword(sword_base)
bread = Food('bread',12)
crystal = Magic('crystal',{'set':{'statuseffect':'CRYSTAL'}},'buff health',req={'hp':180})


'''
punch = Attack('punch',24) 
kick = Attack('kick',24) 
heal = Heal('back away',100)
poison = Statuseffect('POISON',{'nerf':{'hp':10}},repeat_times=6)




bite = Attack('bite',10) 
snatch = Heal('snatch heal',5)
game.player.combat_options.append([snatch])
goblin = Entity('Goblin',100,150,20,10,[bite,snatch],drops={crystal:2})
battle = Battle(game.player,goblin)
battle.start_battle()
'''



























def bar_seq():
	print('bar')

def inn_seq():
	print('inn')

bar = Room('bar',bar_seq)
inn = Room('inn',inn_seq)

villagerooms = [bar,inn]
village = Environment('village',villagerooms)




def fire_sequence(player):
	player.effect = 'fire'

#village.enter()

#skill_tree = {'combat':{'fire':(fire:=Skill('fire','fiery spell',{'looting':0},fire_sequence))}}