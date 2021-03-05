import engine.game as game
from engine.item_system import Weapon, Sword, Consumable, Magic

if __name__ == '__main__':
	game = game.Game('f',0)
	bread = Consumable('bread',10)
	carrot = Consumable('carrot',10)
	game.player.give_item(carrot, 105)	
	game.player.inventory.display()
	
	print(game.player.inventory.total_items(count_stacks=False))

	
	



	
	

