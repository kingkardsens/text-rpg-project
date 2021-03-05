# imports

import pickle
import colorama
from colorama import Fore, Back, Style
colorama.init()




# engine utility, helps test stuff and other handy stuff


def save(content,filename='save'):
	with open('..\\saves\\'+filename+'.sav','wb') as f:
		pickle.dump(content, f, pickle.HIGHEST_PROTOCOL)

def load(filename='save'):
	with open('..\\saves\\'+filename+'.sav','rb') as f:
		content = pickle.load(f)
	return content


# handy variables

variables = {

	'colors':{ 		# colors for coloroma -- #print('{fore[yellow]}{back[magenta]} lol {reset}'.format(**variables['colors']))
		'fore':{'black':Fore.BLACK,'green':Fore.GREEN,'yellow':Fore.YELLOW,'red':Fore.RED,'blue':Fore.BLUE,'magenta':Fore.MAGENTA,'cyan':Fore.CYAN,'white':Fore.WHITE,'reset':Style.RESET_ALL},
		'back':{'black':Back.BLACK,'green':Back.GREEN,'yellow':Back.YELLOW,'red':Back.RED,'blue':Back.BLUE,'magenta':Back.MAGENTA,'cyan':Back.CYAN,'white':Back.WHITE,'reset':Style.RESET_ALL},
		'reset':Style.RESET_ALL
	},


}



# temporary class storage

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








if __name__ == '__main__':
	pass
