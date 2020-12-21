import csv
import random
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

# I think it’d be helpful to create views sorted by engagement score, resources, and date created (descending).
# Eventually we’ll want to create user lists for group moderators to send targeted email campaigns to.
# Those will likely start on a case by case basis, so I’ll let you know when we have a request.

class Directory:
	def __init__(self):
		self.users = []

		self.categories = {}
		self.categories['groups'] = []
		self.categories['expertise'] = []
		self.categories['industry'] = []
		self.categories['interests'] = []
		self.categories['resources'] = []

class User:
	def __init__(self, uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources):
		self.uid = uid #user id
		self.first_name = first_name #tracks name of play
		self.last_name = last_name
		self.email = email
		self.last_active = last_active #date profile was last active
		self.created = created #date profile was created
		self.count = count #number of times signed in
		self.score = score
		self.groups = groups #tracks groups person is associated with
		self.expertise = expertise
		self.industry = industry
		self.interests = interests
		self.resources = resources

def fill_directory(directory, category, data):
	for item in data:
		if item not in directory.categories[category]:
			directory.categories[category].append(item)

def fix_list(data):
	result = []

	for item in data:
		if type(item) == str:
			if len(item) > 0:
				if item[0] == ' ':
					item = item[1:]
		if item != '':
			result.append(item)

	return result

def analysis(directory):
	for user in directory.users:
		print(user.last_name+","+user.first_name+": "+str(user.score))

def read_users(path, directory):
	users = []
	df = pd.read_excel(path)
	df = df.fillna("")
	categories = list(df.columns)
	# print(categories.index("_e63e1ef3_Resources"))
	data = df.to_numpy()
	for row in data:

		uid = row[0]
		first_name = row[7]
		last_name = row[4]
		email = row[10]
		last_active = row[41].split(' ')[0]
		created = row[44].split(' ')[0]
		count = row[40]

		score = 0
		if row[119] != '':
			score = int(row[119])

		groups = fix_list(row[117].split(","))
		fill_directory(directory, 'groups', groups)

		expertise = fix_list(row[124].split(","))
		fill_directory(directory, 'expertise', expertise)

		industry = fix_list(row[128].split(","))
		fill_directory(directory, 'industry', industry)

		interests = fix_list(row[130].split(","))
		fill_directory(directory, 'interests', interests)

		resources = fix_list(row[123].split(","))
		fill_directory(directory, 'resources', resources)

		user = User(uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources)
		users.append(user)

	return users

def get_filename(directory):

	value = ""

	files = [f for f in listdir(directory) if isfile(join(directory, f))]
	options = []

	for file in files:
		if "User_export_" in file:
			date = file.replace("~$","")
			date = date.replace("User_export_","")
			date = date.replace(".xlsx","")
			if date not in options:
				options.append(date)

	if len(options) > 0:

		value = options[0]
		for option in options:
			latest_split = value.split("-")
			curr_split = option.split("-")

			if (int(curr_split[0]) >= int(latest_split[0])) and (int(curr_split[1]) >= int(latest_split[1])) and (int(curr_split[2]) >= int(latest_split[2])):
				value = option

		value = "User_export_" + value + ".xlsx"

	else:
		print("ERROR: No user export files found!")

	return value



#reports
	#industry
		#specific industry
			#list of users sorted by score
	#interests
		#specific interests


def write_file(directory, category):
	file_name = './reports/' + category = '.csv'
	with open(file_name, "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		string = ""
		writer.writerow([string])

def main():


	dir_name = "./data/"
	file_name = get_filename(dir_name)
	path = dir_name + file_name

	directory = Directory()
	directory.users = read_users(path, directory)

	directory.users.sort(key=lambda user:user.score, reverse=True)
	# directory.users = sorted(directory.users, key=lambda user: user.score, reverse=True)
	
	# analysis(directory)



main()