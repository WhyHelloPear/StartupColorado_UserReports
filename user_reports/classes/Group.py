class Group:
	# Object used for single group in the platform
	# Tracks name, group id, and users in each group

	def __init__(self, gid, name):
		self.gid = gid #group id
		self.name = name 
		self.users = [] #holds user objects for users in each group

	def get_active_size(self):
		size = 0
		for user in self.users:
			if user.active:
				size += 1
		return size

	def get_percent_active(self):
		active = self.get_active_size() #get size of active users
		percent = round((active / len(self.users)), 2) * 100 #get percentage of active/total users
		return int(percent) #return int of float