
class Menu:
	def __init__(self, title, options, run=None):
		self.title = title
		self.options = options # {'do this':do_this_function}
		if run:
			self.run = run

	def display(self):
		print(self.title)
		n = 1
		for option in self.options.keys():
			print(f'{n}. {option}')
			n += 1

		print('e. exit')

	def get_choice(self):
		choice = input('> ')
		try:
			choice = int(choice)-1
			if choice < 0 or choice >= len(list(self.options.keys())):
				return False
			else:
				return self.options[list(self.options.keys())[choice]]

		except ValueError:
			if choice.strip().lower() == 'e':
				return True # exit
			else:
				return False

	def close_menu(self):
		print('exited menu')

	def no_such_option(self):
		print('no such option')

	def run(self):
		while True:
			self.display()
			
			choice = self.get_choice()
			if choice == True:
				self.close_menu() # interface part 
				break
			elif choice:
				choice()
			else:
				self.no_such_option()



		
		
