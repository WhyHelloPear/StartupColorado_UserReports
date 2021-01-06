import os
import shutil
import csv
import random
import xlsxwriter
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
		self.groups = []
		self.group_names = {2315:"Help Center",
							2720:"Grand Valley Entrepreneurs",
							2721:"Food and Agriculture Industries",
							2910:"Central Mountain Entrepreneurs",
							2986:"ExSW Entrepreneurs of the Southwest",
							2987:"SoCo Entrpreneurs",
							3094:"Group Moderators",
							3132:"Northeast Small Biz and Entrepreneurs",
							3196:"Northwest Colorado Entrepreneurs",
							3492:"Roaring Fork Valley Startups",
							3507:"San Luis Valley Entrepreneurs",
							3550:"Outdoor Industry Startups",
							3671:"Rural Entrepreneurial Policy Coalition",
							4148:"Delta-Montrose Entrepreneurs"}

		self.categories = {}
		self.categories['groups'] = []
		self.categories['expertise'] = []
		self.categories['industry'] = []
		self.categories['interests'] = []
		self.categories['resources'] = []


class User:
	def __init__(self, uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources, location, stages):
		self.uid = uid #user id
		self.first_name = first_name #tracks name of play
		self.last_name = last_name
		self.email = email
		self.last_active = last_active #date profile was last active
		self.created = created #date profile was created
		self.count = count #number of times signed in
		self.score = score
		

		self.categories = {}
		self.categories['groups'] = groups
		self.categories['expertise'] = expertise
		self.categories['industry'] = industry
		self.categories['interests'] = interests
		self.categories['resources'] = resources
		self.categories['stages'] = stages
		
		self.location = location
		

class Group:
	def __init__(self, gid, name):
		self.gid = gid
		self.name = name
		self.members = []


def get_group(directory, gid):
	value = None
	for group in directory.groups:
		if group.gid == gid:
			value = group
			break
	return value
		

def add_group_member(directory, user, gid):
	gid = int(gid)
	group = get_group(directory, gid)
	if group == None:
		group = Group(gid, directory.group_names[gid])
		directory.groups.append(group)
	group.members.append(user)
	

#Creates and returns a dictionary that holds all groups and the selected demographics of each group
def create_group_dicts(directory):
	
	#create pie chart of composition of each group and the specified areas of interest (locations, industries, etc)
	
	
	#NOTE: Stages (the stage a user is in within their career) is NOT an accurate report. 
	#Not all users, only a select few in fact, have filled this information out.
	#In act, a single user may make up for 4 or 5 different reported stages; keep this in mind
	
	group_dict = {}
	for group in directory.groups:
		
		group_dict[group.gid] = {}
		locations = {}
		industries = {}
		expertises = {}
		resources = {}
		stages = {}

		for user in group.members:
			
			location = user.location.split(",")[0]
			if location not in locations:
				locations[location] = 1
			else:
				locations[location] += 1
				
			for industry in user.categories['industry']:
				if industry not in industries:
					industries[industry] = 1
				else:
					industries[industry] += 1
			
			for expertise in user.categories['expertise']:
				if expertise not in expertises:
					expertises[expertise] = 1
				else:
					expertises[expertise] += 1
			
			for resource in user.categories['resources']:
				if resource not in resources:
					resources[resource] = 1
				else:
					resources[resource] += 1
			
			for stage in user.categories['stages']:
				if stage not in stages:
					stages[stage] = 1
				else:
					stages[stage] += 1 
					
		group_dict[group.gid]["locations"] = dict(sorted(locations.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["industries"] = dict(sorted(industries.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["expertises"] = dict(sorted(expertises.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["resources"] = dict(sorted(resources.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["stages"] = dict(sorted(stages.items(), key=lambda item:item[1], reverse=True))
	
	return group_dict


#Creates and returns a dictionary that holds all groups and the selected demographics of each group
def create_sum_dict(directory):
	
	#create pie chart of composition of each group and the specified areas of interest (locations, industries, etc)
	
	
	#NOTE: Stages (the stage a user is in within their career) is NOT an accurate report. 
	#Not all users, only a select few in fact, have filled this information out.
	#In act, a single user may make up for 4 or 5 different reported stages; keep this in mind
	

	sum_dict = {}

	locations = {}
	industries = {}
	expertises = {}
	resources = {}
	stages = {}

	for user in directory.users:
		
		location = user.location.split(",")[0]
		if location not in locations:
			locations[location] = 1
		else:
			locations[location] += 1
			
		for industry in user.categories['industry']:
			if industry not in industries:
				industries[industry] = 1
			else:
				industries[industry] += 1
		
		for expertise in user.categories['expertise']:
			if expertise not in expertises:
				expertises[expertise] = 1
			else:
				expertises[expertise] += 1
		
		for resource in user.categories['resources']:
			if resource not in resources:
				resources[resource] = 1
			else:
				resources[resource] += 1
		
		for stage in user.categories['stages']:
			if stage not in stages:
				stages[stage] = 1
			else:
				stages[stage] += 1 
				
	sum_dict["locations"] = dict(sorted(locations.items(), key=lambda item:item[1], reverse=True))
	sum_dict["industries"] = dict(sorted(industries.items(), key=lambda item:item[1], reverse=True))
	sum_dict["expertises"] = dict(sorted(expertises.items(), key=lambda item:item[1], reverse=True))
	sum_dict["resources"] = dict(sorted(resources.items(), key=lambda item:item[1], reverse=True))
	sum_dict["stages"] = dict(sorted(stages.items(), key=lambda item:item[1], reverse=True))

	return sum_dict
		

def fill_directory(directory, category, data):
	filtered_data = []
	for item in data:
		if item == 'Outoor Recreation':
			item = 'Outdoor Recreation'
		if item not in directory.categories[category]:
			directory.categories[category].append(item)
		if item not in filtered_data:
			filtered_data.append(item)
	return filtered_data


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
		groups = fill_directory(directory, 'groups', groups)

		expertise = fix_list(row[124].split(","))
		expertise = fill_directory(directory, 'expertise', expertise)

		industry = fix_list(row[128].split(","))
		industry = fill_directory(directory, 'industry', industry)

		interests = fix_list(row[130].split(","))
		interests = fill_directory(directory, 'interests', interests)

		resources = fix_list(row[123].split(","))
		resources = fill_directory(directory, 'resources', resources)

		location = "NO RECORDED LOCATION"
		
		full_address = row[77] #full address
		state = row[79] #city
		
		if len(state) != 0:
			location = state
		else:
			if len(full_address) != 0:
				split = full_address.split(",")
				if len(split) > 3:
					location = split[1]
				else:
					location = split[0]

		
		
		stages = fix_list(row[87].split(","))
		fill_directory(directory, 'groups', groups)

		user = User(uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources, location, stages)
		users.append(user)

		for gid in groups:
			add_group_member(directory, user, gid)

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


			#newer year
			if int(curr_split[0]) > int(latest_split[0]):
				value = option

			#same year
			elif int(curr_split[0]) == int(latest_split[0]):

				#newer month
				if int(curr_split[1]) > int(latest_split[1]):
					value = option

				#same month
				elif int(curr_split[1]) == int(latest_split[1]):

					#newer day
					if int(curr_split[2]) >= int(latest_split[2]):
						value = option

		value = "User_export_" + value + ".xlsx"

	else:
		print("ERROR: No user export files found!")

	return value


def handle_report_folder():
	try:
		shutil.rmtree('./reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder not defined")
	
	try:
		os.mkdir('./reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder already defined")


def generate_group_reports(directory, group_dicts):

	os.mkdir('./reports/group_reports/')

	categories = ['locations','industries','expertises','resources','stages']

	for group in directory.groups:
		gid = group.gid
		name = group.name.replace(' ', '_')

		workbook = xlsxwriter.Workbook('reports/group_reports/'+str(gid)+'_'+name+'.xlsx')
		worksheet = workbook.add_worksheet()


		col = 0
		for category in categories:

			row = 2
			worksheet.write(row-1, col, category)
			worksheet.write(row-1, col+1, 'Count')

			for key in group_dicts[gid][category].keys():

				worksheet.write(row, col, key)
				worksheet.write(row, col+1, group_dicts[gid][category][key])
				row += 1

			col += 3

		merge_format = workbook.add_format({'align': 'center','valign': 'vcenter'})
		worksheet.merge_range('A1:N1', str(gid)+": "+group.name, merge_format)

		workbook.close()


def generate_sum_report(directory, sum_dict):

	# os.mkdir('./reports/group_reports/')

	categories = ['locations','industries','expertises','resources','stages']

	workbook = xlsxwriter.Workbook('reports/sum_report.xlsx')
	worksheet = workbook.add_worksheet()

	col = 0
	for category in categories:

		row = 2
		worksheet.write(row-1, col, category)
		worksheet.write(row-1, col+1, 'Count')

		for key in sum_dict[category].keys():

			worksheet.write(row, col, key)
			worksheet.write(row, col+1, sum_dict[category][key])
			row += 1

		col += 3

	merge_format = workbook.add_format({'align': 'center','valign': 'vcenter'})
	worksheet.merge_range('A1:N1', "User Breakdown", merge_format)

	workbook.close()


def main():

	dir_name = "./data/"
	file_name = get_filename(dir_name)
	path = dir_name + file_name

	directory = Directory()
	directory.users = read_users(path, directory)
	directory.users.sort(key=lambda user:user.score, reverse=True)

	sum_dict = create_sum_dict(directory)
	group_dicts = create_group_dicts(directory)

	handle_report_folder()

	generate_sum_report(directory, sum_dict)
	generate_group_reports(directory, group_dicts)


main()