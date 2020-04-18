class ScrapeError(Exception):
    def __init__(self, type):
    	self.type = type
    def __str__(self):
    	if self.type == 0:
    		return 'Scrape Error: ' + 'Element Not Exist'
    	elif self.type == 1:
    		return 'Scrape Error: ' + 'Page Not Exist'
    	elif self.type == 2:        
    		return 'Scrape Error: ' + 'Invalid Result'
    	else:
    		return 'Scrape Error: ' + 'Others'
class CallError(Exception):
    def __init__(self, type):
    	self.type = type
    def __str__(self):
    	if self.type == 0:
    		return 'Call Error: ' + 'Function Not Exist'
    	elif self.type == 1:
    		return 'Call Error: ' + 'Require Arguement'
    	elif self.type == 2:
    		return 'Call Error: ' + 'Ambigious Function Call'
    	elif self.type == 3:
    		return 'Call Error: ' + 'Invalid Arguement'
    	elif self.type == 4:
    		return 'Call Error: ' + 'Missing Arguement'
    	else:
    		return 'Call Error: ' + 'Others'