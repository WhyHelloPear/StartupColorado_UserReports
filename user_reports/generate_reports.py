import os
from os import listdir
from os.path import isfile, join

import shutil
import csv
import random
import xlsxwriter
import pandas as pd
import numpy as np
import math

from fpdf import FPDF
import pdfkit

# I think it’d be helpful to create views sorted by engagement score, resources, and date created (descending).
# Eventually we’ll want to create user lists for group moderators to send targeted email campaigns to.
# Those will likely start on a case by case basis, so I’ll let you know when we have a request.


class Directory:
	def __init__(self):
		self.users = []
		self.groups = []
		self.group_names = {}
		self.categories = {}
		self.categories['groups'] = []
		self.categories['expertise'] = []
		self.categories['industry'] = []
		self.categories['interests'] = []
		self.categories['resources'] = []
		self.categories['member_types'] = []
		self.current_date = ''


class User:
	def __init__(self, uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources, location, stages, active, member_types):
		self.uid = uid #[STRING]   user id
		self.first_name = first_name #tracks name of play
		self.last_name = last_name
		self.email = email
		self.last_active = last_active #date profile was last active
		self.created = created #date profile was created
		self.count = count # [INT]   number of times signed in
		self.score = score # [INT]
		

		self.categories = {}
		self.categories['groups'] = groups
		self.categories['expertise'] = expertise
		self.categories['industry'] = industry
		self.categories['interests'] = interests
		self.categories['resources'] = resources
		self.categories['stages'] = stages
		self.categories['member_types'] = member_types
		
		self.location = location

		self.active = active
		

class Group:
	def __init__(self, gid, name):
		self.gid = gid
		self.name = name
		self.members = []



#======================================
# HELPER FUNCTIONS
#======================================
def get_max_string_len(data):
	value = 0
	for item in data:
		if len(item) > value:
			value = len(item)
	return value


def get_group(directory, gid):
	value = None
	for group in directory.groups:
		if group.gid == gid:
			value = group
			break
	return value


def get_index(categories, category):
	index = None
	if category in categories:
		index = categories.index(category)

	return index


def add_group_member(directory, user, gid):
	gid = int(gid)
	group = get_group(directory, gid)
	if group == None:
		group = Group(gid, directory.group_names[gid])
		directory.groups.append(group)
	group.members.append(user)


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


def format_date(date):
	date = date.split('-')
	date = date[1]+'/'+date[2]+'/'+date[0]
	return date


#======================================
# MAIN FUNCTIONS
#======================================
	

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
		interests = {}
		resources = {}
		stages = {}
		member_types = {}

		for user in group.members:

			if user.active:
			
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

				for interest in user.categories['interests']:
					if interest not in interests:
						interests[interest] = 1
					else:
						interests[interest] += 1
				
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

				for member_type in user.categories['member_types']:
					if member_type not in member_types:
						member_types[member_type] = 1
					else:
						member_types[member_type] += 1 
					
		group_dict[group.gid]["locations"] = dict(sorted(locations.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["industries"] = dict(sorted(industries.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["expertises"] = dict(sorted(expertises.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["interests"] = dict(sorted(interests.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["resources"] = dict(sorted(resources.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["stages"] = dict(sorted(stages.items(), key=lambda item:item[1], reverse=True))
		group_dict[group.gid]["member_types"] = dict(sorted(member_types.items(), key=lambda item:item[1], reverse=True))

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
	interests = {}
	resources = {}
	stages = {}
	member_types = {}

	for user in directory.users:

		if user.active:
		
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

			for interest in user.categories['interests']:
				if interest not in interests:
					interests[interest] = 1
				else:
					interests[interest] += 1
			
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

			for member_type in user.categories['member_types']:
				if member_type not in member_types:
					member_types[member_type] = 1
				else:
					member_types[member_type] += 1 
				
	sum_dict["locations"] = dict(sorted(locations.items(), key=lambda item:item[1], reverse=True))
	sum_dict["industries"] = dict(sorted(industries.items(), key=lambda item:item[1], reverse=True))
	sum_dict["expertises"] = dict(sorted(expertises.items(), key=lambda item:item[1], reverse=True))
	sum_dict["interests"] = dict(sorted(interests.items(), key=lambda item:item[1], reverse=True))
	sum_dict["resources"] = dict(sorted(resources.items(), key=lambda item:item[1], reverse=True))
	sum_dict["stages"] = dict(sorted(stages.items(), key=lambda item:item[1], reverse=True))
	sum_dict["member_types"] = dict(sorted(member_types.items(), key=lambda item:item[1], reverse=True))


	return sum_dict


def create_diff_group_dict(curr_group_directory, prev_group_directory):

	diff_group_dict = {}

	for gid in curr_group_directory.keys():
		diff_group_dict[gid] = {}
		for category in curr_group_directory[gid].keys():
			category_dict = {}
			for item in curr_group_directory[gid][category].keys():
				diff = 0
				if gid in prev_group_directory:
					if item in prev_group_directory[gid][category]:
						diff = curr_group_directory[gid][category][item] - prev_group_directory[gid][category][item]
					else:
						diff = curr_group_directory[gid][category][item]

				category_dict[item] = diff
			diff_group_dict[gid][category] = category_dict

	return diff_group_dict
		

def create_diff_sum_dict(curr_sum_directory, prev_sum_directory):

	diff_sum_dict = {}

	for category in curr_sum_directory.keys():
		category_dict = {}
		for item in curr_sum_directory[category].keys():
			diff = 0
			if item in prev_sum_directory[category]:
				diff = curr_sum_directory[category][item] - prev_sum_directory[category][item]
			else:
				diff = curr_sum_directory[category][item]

			category_dict[item] = diff
		diff_sum_dict[category] = category_dict

	return diff_sum_dict


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


def read_users(path, directory):
	users = []

	df = pd.read_excel(path)
	df = df.fillna("")

	categories = list(df.columns)

	data = df.to_numpy()

	for row in data:

		uid = ""
		index = get_index(categories, "ID")
		if index != None:
			uid = row[index]

		first_name = ""
		index = get_index(categories, "First name")
		if index != None:
			first_name = row[index]

		last_name = ""
		index = get_index(categories, "Last name")
		if index != None:
			last_name = row[index]

		email = ""
		index = get_index(categories, "Email")
		if index != None:
			email = row[index]

		last_active = ""
		index = get_index(categories, "Last sign in date")
		if index != None:
			last_active = row[index].split(' ')[0]

		created = ""
		index = get_index(categories, "Created at")
		if index != None:
			created = row[index].split(' ')[0]

		#number of times user has signed in (shows if user has activated their account or not)
		count = 0
		index = get_index(categories, "Count of sign in")
		if index != None:
			count = int(row[index])

		active = False
		if count > 0:
			active = True

		score = 0
		index = get_index(categories, "Engagement Scoring:Current score")
		if index != None:
			if row[index] != '':
				score = int(row[index])

		groups = []
		index = get_index(categories, "Groups Member:Group Member")
		if index != None:
			groups = fix_list(row[index].split(","))
			groups = fill_directory(directory, 'groups', groups)

		expertise = []
		index = get_index(categories, "_281d4ac7_Expertise")
		if index != None:
			expertise = fix_list(row[index].split(","))
			expertise = fill_directory(directory, 'expertise', expertise)

		industry = []
		index = get_index(categories, "_07417723_Industry_1")
		if index != None:
			industry = fix_list(row[index].split(","))
			industry = fill_directory(directory, 'industry', industry)

		interests = []
		index = get_index(categories, "_ec0c314f_Resources_I_Am_Interested_In")
		if index != None:
			interests = fix_list(row[index].split(","))
			interests = fill_directory(directory, 'interests', interests)

		resources = []
		index = get_index(categories, "_e63e1ef3_Resources")
		if index != None:
			resources = fix_list(row[index].split(","))
			resources = fill_directory(directory, 'resources', resources)


		location = "NO RECORDED LOCATION"

		full_address = ""
		index = get_index(categories, "Live Location:Address")
		if index != None:
			full_address = row[index] #full address

		city = ""
		index = get_index(categories, "Live Location:City")
		if index != None:
			city = row[index] #city
		
		if len(city) != 0:
			location = city
		else:
			if len(full_address) != 0:
				split = full_address.split(",")
				if len(split) > 3:
					location = split[1]
				else:
					location = split[0]

		stages = []
		index = get_index(categories, "_0318eefd_Business_Stage")
		if index != None:
			stages = fix_list(row[index].split(","))
			fill_directory(directory, 'groups', groups)



		member_types = []
		index = get_index(categories, "SubNetworks:Title")
		if index != None:
			member_types = fix_list(row[index].split(","))
			if "Undefined" in member_types:
				member_types.remove("Undefined")
			fill_directory(directory, 'member_types', member_types)




		user = User(uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests, resources, location, stages, active, member_types)
		users.append(user)

		for gid in groups:
			add_group_member(directory, user, gid)

	return users


def read_group_names(path):
	names = {}
	file_name = path + "names.csv"
	with open(file_name) as file:
		data = csv.reader(file, delimiter=",")
		for row in data:
			gid = int(row[0])
			name = row[1]

			names[gid] = name

	return names


def most_recent_date(d1, d2):

	d1 = d1.split("-")
	d2 = d2.split("-")

	new = d1
	old = d2


	#newer year
	if int(d2[0]) > int(d1[0]):
		new = d2
		old = d1

	#same year
	elif int(d2[0]) == int(d1[0]):

		#newer month
		if int(d2[1]) > int(d1[1]):
			new = d2
			old = d1

		#same month
		elif int(d2[1]) == int(d1[1]):

			#newer day
			if int(d2[2]) >= int(d1[2]):
				new = d2
				old = d1

	new = new[0]+'-'+new[1]+'-'+new[2]
	old = old[0]+'-'+old[1]+'-'+old[2]

	return new, old


def get_dates(path):

	value = ""

	files = [f for f in listdir(path) if isfile(join(path, f))]
	dates = []

	for file in files:
		if "User_export_" in file:
			date = file.replace("~$","")
			date = date.replace("User_export_","")
			date = date.replace(".xlsx","")
			if date not in dates:
				dates.append(date)

	done = False

	while not done:
		previous = dates.copy()

		for i in range(len(dates)):
			if i == len(dates) - 1:
				break

			new, old = most_recent_date(dates[i], dates[i+1])
			dates[i] = new
			dates[i+1] = old

		if dates == previous:
			done = True

	return dates


def handle_report_folder():
	try:
		shutil.rmtree('./reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder not defined")
	
	try:
		os.mkdir('./reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder already defined")


def generate_pdf(name, path):
	options = {
		'page-size': 'A4',
		'margin-top': '0in',
		'margin-right': '0in',
		'margin-bottom': '0in',
		'margin-left': '0in',
		'encoding': "UTF-8",
	}

	output = path + name + ".pdf"
	pdfkit.from_file('./html_report.html', output) 


def split_dict(full_dict, num):

	dicts = []
	keys = list(full_dict.keys())
	items = list(full_dict.values())

	full = len(keys)

	status = 0

	for i in range(num):
		sub_dict = {}

		length = 0
		if i == num-1:
			if num == 3:
				length = full - (math.ceil(full/3) * 2)
			else:
				length = full - math.ceil(full/2)
		else:
			length = math.ceil(full/num)

		for j in range(status,length+status):
			sub_dict[keys[j]] = items[j]

		status += length
		dicts.append(sub_dict)
		
	return dicts


def generate_group_pdf(curr_directory, prev_directory, group_dicts, diff_group_dict):

	try:
		os.mkdir('./reports/group_reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder already defined")

	original_template = ""

	with open('./data/html_template_group.csv', newline='') as csvfile:
		file = csv.reader(csvfile)
		for row in file:
			for item in row:
				original_template += item


	for group in curr_directory.groups:

		template = original_template
		gid = group.gid
		name = group.name

		date = curr_directory.current_date
		
		prev_group = get_group(prev_directory, gid)
		if prev_group != None:
			date += '<br>Previous Report Date: ' + prev_directory.current_date

		size_diff = None
		if prev_directory != None:
			if prev_group != None:
				size_diff = len(group.members) - len(prev_group.members)

		size = str(len(group.members))
		if size_diff != None:
			if size_diff > 0:
				size += '   (+'+str(size_diff)+')'
			elif size_diff < 0:
				size += '   ('+str(size_diff)+')'


		path = "./data/group_data/cover_photos/"
		files = [f for f in listdir(path) if isfile(join(path, f))]
		background_name = "default.jpg"
		# for file in files:
		# 	if str(gid) in file:
		# 		background_name = file
		background = path + background_name

		path = "./data/group_data/logos/"
		files = [f for f in listdir(path) if isfile(join(path, f))]
		logo_name = "default.jpg"
		# for file in files:
		# 	if str(gid) in file:
		# 		logo_name = file
		logo = path + logo_name
		
		categories = ['locations','industries','expertises','interests','stages','member_types']
		group_dict = group_dicts[gid]
		text_dict = {}

		for category in categories:
			sub_dict = group_dict[category]

			#single col tables
			if (category == "stages") or (category == "member_types"):
				text = ''
				for item in sub_dict:
					text += '<tr><td>'+item+'</td>'
					text += '<td class="count">'+str(sub_dict[item])

					if diff_group_dict != None:
						diff = diff_group_dict[gid][category][item]
						if diff < 0:
							text += ' ('+str(diff)+')'
						elif diff > 0:
							text += ' (+'+str(diff)+')'

					text += '</td></tr>'

				text_dict[category] = text

			#double col tables
			else:
				if category == "locations":
					num = 3
				else:
					num = 2
				dicts = split_dict(sub_dict, num)
				for i in range(len(dicts)):
					text = ''
					new_sub_dict = dicts[i]
					for item in new_sub_dict:
						text += '<tr><td>'+item+'</td>'
						text += '<td class="count">'+str(new_sub_dict[item])

						if diff_group_dict != None:
							diff = diff_group_dict[gid][category][item]
							if diff < 0:
								text += ' ('+str(diff)+')'
							elif diff > 0:
								text += ' (+'+str(diff)+')'

						text += '</td></tr>'

					cat = category+"_"+str(i+1)

					text_dict[cat] = text


		template = template.replace('[INSERT GROUP BACKGROUND]', background)
		template = template.replace('[INSERT GROUP LOGO]', logo)
		template = template.replace('[INSERT GROUP TITLE]', name)
		template = template.replace('[INSERT STAGE ENTRIES]', text_dict['stages'])
		template = template.replace('[INSERT MEMBER TYPE ENTRIES]', text_dict['member_types'])
		template = template.replace('[INSERT INTEREST 1 ENTRIES]', text_dict['interests_1'])
		template = template.replace('[INSERT INTEREST 2 ENTRIES]', text_dict['interests_2'])
		template = template.replace('[INSERT LOCATION 1 ENTRIES]', text_dict['locations_1'])
		template = template.replace('[INSERT LOCATION 2 ENTRIES]', text_dict['locations_2'])
		template = template.replace('[INSERT LOCATION 3 ENTRIES]', text_dict['locations_3'])
		template = template.replace('[INSERT EXPERTISE 1 ENTRIES]', text_dict['expertises_1'])
		template = template.replace('[INSERT EXPERTISE 2 ENTRIES]', text_dict['expertises_2'])
		template = template.replace('[INSERT INDUSTRY 1 ENTRIES]', text_dict['industries_1'])
		template = template.replace('[INSERT INDUSTRY 2 ENTRIES]', text_dict['industries_2'])
		template = template.replace('[INSERT NUM USERS]', size)
		template = template.replace('[INSERT DATE]', date)


		html = open("./html_report.html","w")
		html.write(template)
		html.close()

		file_name = name.replace(' ','_')
		file_name = str(gid) + '_' + file_name

		path = './reports/group_reports/'
		generate_pdf(file_name, path)

		if os.path.exists("./html_report.html"):
			os.remove("./html_report.html")


def generate_sum_pdf(curr_directory, prev_directory, sum_dict, diff_sum_dict):

	template = ""

	with open('./data/html_template_sum.csv', newline='') as csvfile:
		file = csv.reader(csvfile)
		for row in file:
			for item in row:
				template += item


	name = "User Sum Report"
	background = "./data/group_data/cover_photos/default.jpg"
	logo = "./data/group_data/logos/default.jpg"


	date = curr_directory.current_date
	if prev_directory != None:
		date += '<br>Previous Report Date: ' + prev_directory.current_date

	size_diff = None
	if prev_directory != None:
		size_diff = len(curr_directory.users) - len(prev_directory.users)

	size = str(len(curr_directory.users))
	if size_diff != None:
		if size_diff > 0:
			size += '   (+'+str(size_diff)+')'
		elif size_diff < 0:
			size += '   ('+str(size_diff)+')'

	
	categories = ['locations','industries','expertises','interests','stages','member_types']
	text_dict = {}

	for category in categories:
		sub_dict = sum_dict[category]

		#single col tables
		if (category == "stages") or (category == "member_types"):
			text = ''
			for item in sub_dict:
				text += '<tr><td>'+item+'</td>'
				text += '<td class="count">'+str(sub_dict[item])

				if diff_sum_dict != None:
					diff = diff_sum_dict[category][item]
					if diff < 0:
						text += ' ('+str(diff)+')'
					elif diff > 0:
						text += ' (+'+str(diff)+')'

				text += '</td></tr>'

			text_dict[category] = text

		#double col tables
		else:
			if category == "locations":
				num = 3
			else:
				num = 2
			dicts = split_dict(sub_dict, num)
			for i in range(len(dicts)):
				text = ''
				new_sub_dict = dicts[i]
				for item in new_sub_dict:
					text += '<tr><td>'+item+'</td>'
					text += '<td class="count">'+str(new_sub_dict[item])

					if diff_sum_dict != None:
						diff = diff_sum_dict[category][item]
						if diff < 0:
							text += ' ('+str(diff)+')'
						elif diff > 0:
							text += ' (+'+str(diff)+')'

					text += '</td></tr>'

				cat = category+"_"+str(i+1)

				text_dict[cat] = text


	template = template.replace('[INSERT GROUP BACKGROUND]', background)
	template = template.replace('[INSERT GROUP LOGO]', logo)
	template = template.replace('[INSERT GROUP TITLE]', name)
	template = template.replace('[INSERT STAGE ENTRIES]', text_dict['stages'])
	template = template.replace('[INSERT MEMBER TYPE ENTRIES]', text_dict['member_types'])
	template = template.replace('[INSERT INTEREST 1 ENTRIES]', text_dict['interests_1'])
	template = template.replace('[INSERT INTEREST 2 ENTRIES]', text_dict['interests_2'])
	template = template.replace('[INSERT LOCATION 1 ENTRIES]', text_dict['locations_1'])
	template = template.replace('[INSERT LOCATION 2 ENTRIES]', text_dict['locations_2'])
	template = template.replace('[INSERT LOCATION 3 ENTRIES]', text_dict['locations_3'])
	template = template.replace('[INSERT EXPERTISE 1 ENTRIES]', text_dict['expertises_1'])
	template = template.replace('[INSERT EXPERTISE 2 ENTRIES]', text_dict['expertises_2'])
	template = template.replace('[INSERT INDUSTRY 1 ENTRIES]', text_dict['industries_1'])
	template = template.replace('[INSERT INDUSTRY 2 ENTRIES]', text_dict['industries_2'])
	template = template.replace('[INSERT NUM USERS]', size)
	template = template.replace('[INSERT DATE]', date)



	html = open("./html_report.html","w")
	html.write(template)
	html.close()

	file_name = name.replace(' ','_')
	path = './reports/'
	generate_pdf(file_name, path)

	if os.path.exists("./html_report.html"):
		os.remove("./html_report.html")


def main():
	handle_report_folder()

	export_dir_name = "./data/user_exports/"
	dates = get_dates(export_dir_name)

	curr_date = None
	prev_date = None
	if len(dates) == 0:
		print("ERROR: No use exports found in data directory!")
		return(0)
	else:
		curr_date = dates[0]
		if len(dates) > 1:
			prev_date = dates[1]

	curr_date = format_date(curr_date)

	export_name = "User_export_" + dates[0] + ".xlsx"
	export_path = export_dir_name + export_name

	curr_directory = Directory()
	curr_directory.current_date = curr_date

	group_dir_name = "./data/group_data/"
	curr_directory.group_names = read_group_names(group_dir_name)
	
	curr_directory.users = read_users(export_path, curr_directory)
	curr_directory.users.sort(key=lambda user:user.score, reverse=True)

	curr_sum_dict = create_sum_dict(curr_directory)
	curr_group_dicts = create_group_dicts(curr_directory)

	diff_group_dict = None
	prev_directory = None

	if prev_date != None:
		prev_date = format_date(prev_date)
		export_name = "User_export_" + dates[1] + ".xlsx"
		export_path = export_dir_name + export_name
		prev_directory = Directory()
		prev_directory.current_date = prev_date

		prev_directory.group_names = read_group_names(group_dir_name)

		prev_directory.users = read_users(export_path, prev_directory)
		prev_directory.users.sort(key=lambda user:user.score, reverse=True)

		prev_sum_dict = create_sum_dict(prev_directory)
		prev_group_dicts = create_group_dicts(prev_directory)

		diff_group_dict = create_diff_group_dict(curr_group_dicts, prev_group_dicts)
		diff_sum_dict = create_diff_sum_dict(curr_sum_dict, prev_sum_dict)

	generate_group_pdf(curr_directory, prev_directory, curr_group_dicts, diff_group_dict)
	generate_sum_pdf(curr_directory, prev_directory, curr_sum_dict, diff_sum_dict)


main()