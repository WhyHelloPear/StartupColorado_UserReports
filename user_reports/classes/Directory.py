from classes.DesiredContent import DesiredContent

_desired_content = DesiredContent()
_test = []

class Directory:
	# Directory is the main access point to all objects generated from User Exports
	# Including User and Group objects that are used later to genereate the reports

	def __init__(self):
		self.users = [] #holds user objects
		self.groups = [] #holds group objects
		self.group_names = {} #holds names of groups
		self.categories = {}
		self.categories['groups'] = []
		self.categories['expertise'] = []
		self.categories['industry'] = []
		self.categories['interests'] = []
		self.categories['resources'] = []
		self.categories['stages'] = []
		self.categories['member_types'] = []
		self.current_date = '' #holds date of directory


	#fills specified directory dictionary with given data
	def fill_directory(directory, category, data):
		filtered_data = [] #ensures returned data are not duplicates 
		for item in data: 
			item = _desired_content.MapContent(item)		
			if item not in directory.categories[category]: #adds new item to directory dictionary
				directory.categories[category].append(item)
			if item not in filtered_data: #adds new item to returned list
				filtered_data.append(item)
		return filtered_data #returns non-duplicated data


	def get_active_size(self):
		size = 0
		for user in self.users:
			if user.active:
				size += 1
		return size


	#returns percentage of active users of a directory
	def get_percent_active(self):
		active = self.get_active_size() #get size of active users
		percent = round((active / len(self.users)), 2) * 100 #get percentage of active/total users
		return int(percent) #return int of float