class User:
	# User objects are created for each user in the export file
	# Holds selected information about a single user that is used in later reports

	def __init__(self, uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources, location, stages, active, member_types):
		self.uid = uid #[STRING] user id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.last_active = last_active #date profile was last active
		self.created = created #date profile was created
		self.count = int(count) # [INT] number of times signed in
		self.score = int(score) # [INT] user activity score
		self.categories = {}
		self.categories['groups'] = groups
		self.categories['expertise'] = expertise
		self.categories['industry'] = industry
		self.categories['interests'] = interests
		self.categories['resources'] = resources
		self.categories['stages'] = stages
		self.categories['member_types'] = member_types
		self.location = location #live location used in reports
		self.active = active #tracks whether user has activated their account or not