import colorama
from colorama import Fore, Back, Style
colorama.init()


class Gameclock:
	def __init__(self,time=0,tickrate=1,day=1,dayrate=20,timesofday=['morning','afternoon','evening','night'],numday=0):
		self.totaltime = time
		self.time = time # 0 time
		self.day = day # day 1
		self.tickrate = tickrate # 1 tick per tick()
		self.timesofday = timesofday # morning, afternoon etc.
		self.timeofdayrate = dayrate # ticks to change time of day
		self.dayrate = self.timeofdayrate*len(self.timesofday) # ticks to change day
		self.timeofday = self.timesofday[numday] # set time of day to whatever specified

	def tick(self,tickamount=1):
		for i in range(tickamount):
			self.time += self.tickrate
			self.totaltime += self.tickrate
			if self.time >= self.dayrate: # if day over, inc day and set time to 0
				self.day += 1
				self.time = 0
				self.timeofday = self.timesofday[0]
			elif self.time % self.timeofdayrate == 0: # if time of day ends change time of day
				index = self.timesofday.index(self.timeofday)
				index += 1
				if index > len(self.timesofday)-1:
					index = 0
				self.timeofday = self.timesofday[index]

	def reset(self,param=None, value=None):
		if not param:
			self.time = 0
			self.totaltime = 0
			self.day = 0
			self.timeofday = self.timesofday[0]
		else:
			param = param.strip()
			if param in self.__dict__.keys():
				if not value:
					self.__dict__[param] = 0
				else:
					self.__dict__[param] = value

	def stats(self,color=None):
		if not color:
			print(f' TIME: {self.time}, DAY: {self.day}, TIME OF DAY: {self.timeofday}, TOTAL TIME: {self.totaltime}')
		else:
			y = Back.YELLOW+Fore.BLACK
			s = Style.RESET_ALL
			print(f' {y} TIME {s}: {self.time}, {y} DAY {s}: {self.day}, {y} TIME OF DAY {s}: {self.timeofday}, {y} TOTAL TIME {s}: {self.totaltime}')
		print()



if __name__ == '__main__':
	clock = Gameclock()
	clock.tick()
	clock.stats(True)


