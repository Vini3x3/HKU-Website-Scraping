class ScrapeError(Exception):
	def __init__(self, type):
		# setting
		self.name = 'Scrape Error'

		# copy argument
		self.type = type

	def __str__(self):
		if self.type == 0:
			return self.name + ': ' + 'Element Not Exist'
		elif self.type == 1:
			return self.name + ': ' + 'Page Not Exist'
		elif self.type == 2:
			return self.name + ': ' + 'Invalid Result'
		else:
			return self.name + ': ' + 'Others'


class CallError(Exception):
	def __init__(self, type):
		# setting
		self.name = 'Call Error'

		# copy argument
		self.type = type

	def __str__(self):
		if self.type == 0:
			return self.name + ': ' + 'Function Not Exist'
		elif self.type == 1:
			return self.name + ': ' + 'Require Arguement'
		elif self.type == 2:
			return self.name + ': ' + 'Ambigious Function Call'
		elif self.type == 3:
			return self.name + ': ' + 'Invalid Arguement'
		elif self.type == 4:
			return self.name + ': ' + 'Missing Arguement'
		else:
			return self.name + ': ' + 'Others'
