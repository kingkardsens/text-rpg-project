import data.interface.menu as menu # import interface into content


def option():
	print('hello')

menu1 = menu.Menu('This is a menu TItle', {'option 1':option, 'option 2':option})