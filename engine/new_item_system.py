class Item:
	def __init__(self, name, stackable=True, use=None):
		self.name = name
		self.stackable = stackable
		self.use_function = use

	def use(self, **kwargs):
		return self.use_function(kwargs)
