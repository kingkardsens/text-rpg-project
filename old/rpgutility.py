# files usually imported: 13, 20, 21, 22, 27, rpgutility
# files that only import files: 28

import pickle
from os import path

save_extension = 'sav'
config_file = 'config.txt'
default_save = 'test21rpg'


settings = {
	'version':'[testing version]',
	'divider':' '+'-'*90, # make settings be individual to a player save
	'title':'RPG MENU',
	'playerdefined':{
		'random_map':True	
	}
	
}

def getfromconfig(attr):
	config = open(config_file,'r')
	for line in config: # current save file
		if attr in line:
			return line
	

def writetoconfig(attr,value):
	config = open(config_file,'r')
	lines = config.readlines()
	config = open(config_file,'w')
	for line in lines:
		if attr in line:
			lines[lines.index(line)] = attr+'='+value
			config.writelines(lines)
			config.close()

def getcfile():
	cfile = getfromconfig('cfile').split('=')[1].split(' ')[0]
	return cfile

def changesave(param,value,file=default_save):
	with open(file+'.'+save_extension,'rb') as f:
	    loaded_game = pickle.load(f)
	loaded_game[param] = value
	with open(file+'.'+save_extension,'wb') as f:
		pickle.dump(loaded_game, f, pickle.HIGHEST_PROTOCOL)

def fileexists(filename,dir_=''):
	if path.isfile(dir_+filename):
		return True
	else:
		return False

def make_config():
	if not fileexists(config_file):
		config = open(config_file,'w')
		config.write('cfile= ')
		config.close()

make_config()