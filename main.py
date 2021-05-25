import engine.game as game
from engine.new_item_system import Item

"""
GAME
  - save -> works
  - load -> works
  - time -> works
  
  PLAYER
    - player location
    - functions to change player parameters (hp, mp etc.)
    - level system (judges what remains locked and what is unlocked)
    - weapon and item slots -> works
    - available base attacks (depend on base player class, rest come with weapons)
    - mastery and stat points (mastery and stat points increase player parameters, will need a mechanism to increment parameters after point allotment)
	- stamina points (decrease with movement, attacking and defense)

    INVENTORY
      - add items to stacks -> works
      - remove items from stacks -> works
      - use items
      - salvage items
      - store and manipulate currency

    BANK
      - cant be accessed until enters location "bank"
      - all inventory traits (exclude salvage items)
      - item and currency storage limit
"""



g = game.Game('Poke',100)

def potion(kwargs):
	try:
		text = kwargs['text']
	except KeyError:
		return False

i = Item('Potion', use=potion)
g.player.give_item(i, 100)

for item in g.player.inventory.item_list:
	if not i.use(on='hello'):
		print('this item is not an attack')
















