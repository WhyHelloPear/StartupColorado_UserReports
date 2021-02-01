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


def get_index(categories, category):
	index = None
	if category in categories:
		index = categories.index(category)

	return index


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


		date = value
		value = "User_export_" + date + ".xlsx"

	else:
		print("ERROR: No user export files found!")


	date = date.split('-')
	month = date[1]
	if month[0] == '0':
		month = month[1:]
	date = month + '/' + date[2] + '/' + date[0]

	return value, date


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

	categories = ['locations','industries','expertises','interests','stages','member_types']

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
		worksheet.merge_range('A1:Q1', str(gid)+": "+group.name, merge_format)

		workbook.close()


def generate_sum_report(directory, sum_dict):

	# os.mkdir('./reports/group_reports/')

	categories = ['locations','industries','expertises','interests','stages','member_types']

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
	worksheet.merge_range('A1:Q1', "User Breakdown", merge_format)

	workbook.close()


def get_max_string_len(data):
	value = 0
	for item in data:
		if len(item) > value:
			value = len(item)
	return value


def generate_pdf(name):
	options = {
		'page-size': 'A4',
		'margin-top': '0in',
		'margin-right': '0in',
		'margin-bottom': '0in',
		'margin-left': '0in',
		'encoding': "UTF-8",
	}

	output = './reports/group_reports/'+ name + ".pdf"
	pdfkit.from_file('./html_report.html', output) 


def get_differences():
	



def write_html(directory, group_dicts):

	try:
		os.mkdir('./reports/group_reports')
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: reports folder already defined")

	original_template = ""

	with open('./data/html_template.csv', newline='') as csvfile:
		file = csv.reader(csvfile)
		for row in file:
			for item in row:
				original_template += item


	for group in directory.groups:

		template = original_template
		gid = group.gid
		name = group.name

		path = "./data/group_data/cover_photos/"
		files = [f for f in listdir(path) if isfile(join(path, f))]
		background_name = "default.jfif"
		for file in files:
			if str(gid) in file:
				background_name = file
		background = path + background_name

		path = "./data/group_data/logos/"
		files = [f for f in listdir(path) if isfile(join(path, f))]
		logo_name = "default.jpg"
		for file in files:
			if str(gid) in file:
				logo_name = file
		logo = path + logo_name
		
		categories = ['locations','industries','expertises','interests','stages','member_types']
		group_dict = group_dicts[gid]
		text_dict = {}

		for category in categories:
			sub_dict = group_dict[category]

			text = ''

			if (category == 'stages') or (category == 'member_types'):
				for item in sub_dict:
					text += '<tr><td>'+item+'</td>'
					text += '<td class="count">'+str(sub_dict[item])+'</td></tr>'
			else:
				items, counts = 

			text_dict[category] = text

		template = template.replace('[INSERT GROUP BACKGROUND]', background)
		template = template.replace('[INSERT GROUP LOGO]', logo)
		template = template.replace('[INSERT GROUP TITLE]', name)
		template = template.replace('[INSERT STAGE ENTRIES]', text_dict['stages'])
		template = template.replace('[INSERT MEMBER TYPE ENTRIES]', text_dict['member_types'])
		template = template.replace('[INSERT INTEREST ENTRIES]', text_dict['interests'])
		template = template.replace('[INSERT LOCATION ENTRIES]', text_dict['locations'])
		template = template.replace('[INSERT EXPERTISE ENTRIES]', text_dict['expertises'])
		template = template.replace('[INSERT INDUSTRY ENTRIES]', text_dict['industries'])

		template = template.replace('[INSERT NUM USERS]', str(len(group.members)))
		template = template.replace('[INSERT DATE]', directory.current_date)

		html = open("./html_report.html","w")
		html.write(template)
		
		name = name.replace(' ','_')
		html_name = str(gid)+'_'+name
		html.close()

		file_name = name.replace(' ','_')
		file_name = str(gid) + '_' + file_name
		generate_pdf(file_name)

		if os.path.exists("./html_report.html"):
			os.remove("./html_report.html")


def main():

	export_dir_name = "./data/user_exports/"
	export_name, date = get_filename(export_dir_name)
	export_path = export_dir_name + export_name

	directory = Directory()
	directory.current_date = date

	group_dir_name = "./data/group_data/"
	directory.group_names = read_group_names(group_dir_name)
	
	directory.users = read_users(export_path, directory)
	directory.users.sort(key=lambda user:user.score, reverse=True)

	sum_dict = create_sum_dict(directory)
	group_dicts = create_group_dicts(directory)

	handle_report_folder()

	# generate_sum_report(directory, sum_dict)
	# generate_group_reports(directory, group_dicts)

	# generate_pdf(directory, group_dicts)


	write_html(directory, group_dicts)


main()


#SDDC