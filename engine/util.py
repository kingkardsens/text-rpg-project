
# stuff left: idk lmao

# imports

import pickle
import colorama
from os import system, name 
from colorama import Fore, Back, Style
colorama.init()




# engine utility, helps test stuff and other handy stuff

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

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





if __name__ == '__main__':
	pass
