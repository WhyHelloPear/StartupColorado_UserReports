import os
import csv
import math
import pdfkit
import pandas as pd
from os import listdir
from os.path import isfile, join
from classes.User import User
from classes.Group import Group
from classes.Directory import Directory
from classes.DesiredContent import DesiredContent

#======================================
# MAIN FUNCTION
#======================================
_desired_content = DesiredContent()

def main():

	try:
		error = check_dates() #checks exports exist
		if not error:
			error = check_reports() #check all pdfs are closed; removes all prev reports
			if not error:
				error = check_groups() #checks if all group names and ids are saved
				if not error:

					print("\n\n\nGenerating all reports...\n")

					curr_directory, prev_directory = fetch_directories() #get directories from user exports

					curr_sum_dict, curr_group_dict = fetch_dicts(curr_directory) #get dicts from current export
					prev_sum_dict, prev_group_dict = fetch_dicts(prev_directory) #get dicts from previous export

					diff_sum_dict, diff_group_dict = fetch_diff_dicts(curr_directory, curr_group_dict, curr_sum_dict, prev_group_dict, prev_sum_dict) #get diff dicts based on curr/prev dicts

					generate_reports(curr_directory, prev_directory, curr_sum_dict, diff_sum_dict, curr_group_dict, diff_group_dict) #generate pdf reports
	
					print("\n All reports have been generated :)\n")

	except OSError as e:
		pass

	input("\nPress 'Enter' to close window...")

#======================================
# HELPER FUNCTIONS
#======================================
def get_max_string_len(data):
	# Simply returns the max length of a string in a list of strings

	value = 0
	for item in data:
		if len(item) > value:
			value = len(item)
	return value


def get_group(directory, gid):
	# returns a group objects from specified gid from directory

	value = None
	if directory != None:
		for group in directory.groups:
			if group.gid == gid: #if group object is found
				value = group
				break #break loop and return group object
	return value


def get_index(categories, category):
	#returns the index of a category in the excel file

	index = ""
	if category in categories:
		index = categories.index(category)

	return index


def add_group_member(directory, user, gid):
	#adds user object to a group object's member list
	gid = int(gid)
	group = get_group(directory, gid) #gets group object from group id
	if group == None: #if group has not been created yet...
		group = Group(gid, directory.group_names[gid]) #create the group
		directory.groups.append(group) #add group to the directory
	group.users.append(user) #add user to the group


def fix_list(data):
	#formats a list correctly to remove unnecessary characters and spaces

	result = [] #resulting list

	for item in data:#iterate over every item in original list
		if type(item) == str:
			if len(item) > 0:
				if item[0] == ' ': #removes unecessary space at start of string
					item = item[1:]
		if item != '':
			result.append(item)

	return result


def format_date(date):
	#formats a date correctly in form of mm/dd/yyyy

	date = date.split('-')
	date = date[1]+'/'+date[2]+'/'+date[0]
	return date


def split_dict(full_dict, num):
	#splits a dictionary into several dictionaries based on given size, 'num'
	#a single directory may be split into 2, 3, or 4 dictionaries for example

	dicts = [] #list of final dictionaries
	keys = list(full_dict.keys()) #gets all keys of original dictionary into a list
	items = list(full_dict.values()) #gets all values of original dictionary into a list
	full = len(keys) #length of original dictionary
	status = 0 #tracks how many keys/values have been handled already, initially 0

	for i in range(num): #loops for number of desired dictionaries
		sub_dict = {} #sub-dictionary for a single loop
		length = 0 #tracks length of current sub-dictionary
		if i == num-1: #if current dictionary is the last sub-dictionary
			if num == 3: #formats length of final sub-dict
				length = full - (math.ceil(full/3) * 2)
			else:
				length = full - math.ceil(full/2)
		else:
			length = math.ceil(full/num)

		for j in range(status,length+status): #fill sub-dictionary with un-used keys/values
			if j >= full: #ensures index is not out of range
				break
			sub_dict[keys[j]] = items[j] #add item to sub-dict

		status += length #update number of keys/values handled for next iteration
		dicts.append(sub_dict) #add sub-dict to final list of dictionaries
		
	return dicts


def most_recent_date(d1, d2):
	#returns the most recent date of two given dates

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


def get_curr_date():
	#Gets the most recent date in export list; only call if export existence has been confirmed (check_dates())
	curr_date = get_dates("./data/user_exports/")[0];
	year = curr_date[:6]
	curr_date = curr_date[5:] + '-' + curr_date[:4]
	curr_date = curr_date.replace('-','_')
	return curr_date


#======================================
# PRIMARY FUNCTIONS
#======================================
def get_dates(path):
	#gets all dates from all saved user export files and sorts dates from newest to oldest

	value = ""

	files = [f for f in listdir(path) if isfile(join(path, f))] #gets names of all files in export directory
	dates = []

	for file in files:
		if "User_export_" in file: #if file is a user export
			date = file.replace("~$","") #format
			date = date.replace("User_export_","") #format
			date = date.replace(".xlsx","") #format
			if date not in dates: #check date is not already stored in final list
				dates.append(date)

	done = False #ensures loop repeats until all dates are correctly sorted from most recent to oldest

	#bubble sort
	while not done:
		previous = dates.copy() #used to check if list has not changed from start of loop to the end

		for i in range(len(dates)):
			if i == len(dates) - 1:
				break

			new, old = most_recent_date(dates[i], dates[i+1])
			dates[i] = new
			dates[i+1] = old

		if dates == previous: #if list is the same from the start of the loop...
			done = True #list is correctly sorted and loop can end

	return dates


def read_group_names(path):
	#reads saved group names and id's from file into our directory for later use

	names = {} #matches group id's to group names
	file_name = path + "names.csv" #file directory from specified path
	with open(file_name) as file:
		data = csv.reader(file, delimiter=",") 
		for row in data: #go over every saved group name
			gid = int(row[0]) #get group id
			name = row[1] #get group name
			names[gid] = name #save data to dictionary

	return names


def read_users(path, directory):
	#item creates user objects and adds created user objects to given directory object

	users = [] #holds user objects

	df = pd.read_excel(path) #get data from user export
	df = df.fillna("") #fills empty entries with empty strings

	categories = list(df.columns) #gets all categories from file

	data = df.to_numpy() #converts dataframe to an array

	fields = [ #list of all desired fields/data to be saved in user object
		"ID",
		"First name",
		"Last name",
		"Email",
		"Last sign in date",
		"Created at",
		"Count of sign in",
		"Engagement Scoring:Current score",
		"Groups Member:Group Member",
		"_281d4ac7_Expertise",
		"_07417723_Industry_1",
		"_ec0c314f_Resources_I_Am_Interested_In",
		"_e63e1ef3_Resources",
		"_0318eefd_Business_Stage",
		"SubNetworks:Title",
		"Live Location:Address",
		"Live Location:City"
	]

	lists = [ #these fields/data are lists of data
		"Groups Member:Group Member",
		"_281d4ac7_Expertise",
		"_07417723_Industry_1",
		"_ec0c314f_Resources_I_Am_Interested_In",
		"_e63e1ef3_Resources",
		"_0318eefd_Business_Stage",
		"SubNetworks:Title"
	]

	for row in data:
		info = []

		user_data = { #dictionary of user object data with default values
			"uid": "",
			"first_name": "",
			"last_name": "",
			"email": "",
			"last_active": "",
			"created": "",
			"count": "0",
			"score": "0",
			"groups": [],
			"expertise": [],
			"industry": [],
			"interests": [],
			"resources": [],
			"stages": [],
			"member_types": [],
			"full_address": "",
			"city": "",
		}

		#list used to access directory sub-dictionaries
		list_categories = ["groups","expertise","industry","interests","resources","stages","member_types"]

		keys = list(user_data.keys())
		for i in range(len(fields)):
			field = fields[i] 
			index = get_index(categories, field) #gets index of desired data field from export data
			entry = user_data[keys[i]] #default value of user data based on previous declared dictionary value

			if index != "": #if desired category exists in user export file

				if row[index] != "": #if entry of desired category is not empty

					if (field == "Last sign in date") or (field == "Created at"): #ensures data format
						entry = row[index].split(' ')[0]

					elif field in lists: #ensures list data is formatted properly
						fixed_list = fix_list(row[index].split(","))
						if (field == "SubNetworks:Title") and ("Undefined" in fixed_list):
							fixed_list.remove("Undefined")
						entry = directory.fill_directory(list_categories.pop(0), fixed_list)

					else: #data needs no formatting and can be saved directly
						entry = row[index]

			user_data[keys[i]] = entry #saves entry data to user data dictionary

		if int(user_data["count"]) > 0: #if user has signed in at least once...
			active = True #they are considered an active user
		else:
			active = False

		user_data["active"] = active

		#Code below correctly formats a user's location
		location = "NO RECORDED LOCATION" #defualt location
		city = user_data["city"]
		full_address = user_data["full_address"]
		if len(city) != 0: 
			location = city #user's preferred location is their city
		else: #if city is not stored, location is based off their full address
			if len(full_address) != 0:
				split = full_address.split(",")
				if len(split) > 3:
					location = split[1]
				else:
					location = split[0]
		user_data["location"] = location


		user = User( #creates user object based off saved user data
			user_data["uid"],
			user_data["first_name"],
			user_data["last_name"],
			user_data["email"],
			user_data["last_active"],
			user_data["created"],
			user_data["count"],
			user_data["score"],
			user_data["groups"],
			user_data["expertise"],
			user_data["industry"],
			user_data["interests"],
			user_data["resources"],
			user_data["location"],
			user_data["stages"],
			user_data["active"],
			user_data["member_types"]
		)
		users.append(user) #adds user object to list
		for gid in user_data["groups"]: #if user is in group, add user to saved group
			add_group_member(directory, user, gid)

	return users #return list of created user objects


def generate_pdf(html, gid, name, path):
	#Generates a pdf in specefied path based off of created HTML string
	#NOTE: html string is saved to file in order to properly include images in the pdf reports

	options = { #formatting options of PDF
		'page-size': 'A4',
		'margin-top': '0in',
		'margin-right': '0in',
		'margin-bottom': '0in',
		'margin-left': '0in',
		'quiet': '',
		}

	curr_date = get_curr_date()


	file = open("./data/html_report.html","w") #creates html files
	file.write(html) #writes html content from string to files
	file.close() #closes file

	print("Generating " + name + " report...", end="") #state pdf is being created

	if gid != None: #check if file is group report or sum report
		name = name.replace(' ', '_') #format name
		name = str(gid) + '_' + name #format name

	output = path + name + '_[' + curr_date + ']' + ".pdf" #output name for file

	pdfkit.from_file("./data/html_report.html", output, options) #create pdf from html

	print("Done!")

	os.remove("./data/html_report.html") #remove html file


def generate_html(curr_directory, prev_directory, orig_dict, diff_dict, html_type):
	#Generates a string with html code that is used for the reports
	#html_type specifies if html is for group or sum report

	name = "" #title for page
	size = None #number of users
	size_diff = None #difference of users from last report
	active = None #percent of active users 
	active_diff = None #difference of active users from last report
	curr_group = None
	prev_group = None

	banner = "./group_data/banner.jpg"
	logo = "./group_data/logo.jpg"

	html_name = "" #html template file to be loaded

	date = curr_directory.current_date #date of report
	prev_date = "N/A" #default if no previous report exists

	if html_type == "sum": #if report is a user sum report
		name = "User Sum Report" #change title
		html_name = './data/templates/html_template_sum.csv' #dictate sum template will be used

		size = str(curr_directory.get_active_size()) #number of active users in entire directory
		active = str(curr_directory.get_percent_active())
		if prev_directory != None: #check if previous user export file exists
			size_diff = int(size) - prev_directory.get_active_size() #get difference in size
			active_diff = int(active) - prev_directory.get_percent_active()

			prev_date = prev_directory.current_date #write last report date in html

	else: #if report is a group report
		html_name = './data/templates/html_template_group.csv' #load group template
		curr_group = get_group(curr_directory, html_type) #get current group from group id
		prev_group = get_group(prev_directory, html_type) #get group from last report if it exists

		name = curr_group.name #title changes to group name
		size = str(curr_group.get_active_size()) #number of users in group
		active = str(curr_group.get_percent_active())
		if prev_group != None: #if group existed in last user export
			prev_date = prev_directory.current_date
			size_diff = int(size) - prev_group.get_active_size()
			active_diff = int(active) - prev_group.get_percent_active() #difference in % of active users

	active = active + '%'

	template = "" #string used to hold all html code
	with open(html_name, newline='') as csvfile: #writes code from template into string
		file = csv.reader(csvfile)
		for row in file:
			for item in row:
				template += item

	if size_diff != None: #writes change in number of users on report
		if size_diff > 0:
			size += '   (+'+str(size_diff)+')'
		elif size_diff < 0:
			size += '   ('+str(size_diff)+')'

	if active_diff != None: #writes change in number of users on report
		if active_diff > 0.0:
			active += '   (+'+str(active_diff)+'%)'
		elif active_diff < 0.0:
			active += '   ('+str(active_diff)+'%)'
	
	categories = ['locations','industries','expertises','interests','stages','member_types'] #category tables in report
	text_dict = {} #holds text for each table

	for category in categories: #iterate over all categories
		sub_dict = orig_dict[category] #

		#single col tables
		if (category == "stages") or (category == "member_types"):
			text = ''
			for item in sub_dict:
				text += '<tr><td>'+item+'</td>'
				text += '<td class="count">'+str(sub_dict[item])

				if diff_dict != None:
					diff = diff_dict[category][item]
					if diff < 0:
						text += ' ('+str(diff)+')'
					elif diff > 0:
						text += ' (+'+str(diff)+')'

				text += '</td></tr>'

			text_dict[category] = text

		#double (or more) col tables
		else:
			if category == "locations":
				num = 4
			else:
				num = 2
			dicts = split_dict(sub_dict, num)
			for i in range(len(dicts)):
				text = ''
				new_sub_dict = dicts[i]
				for item in new_sub_dict:
					text += '<tr><td>'+item+'</td>'
					text += '<td class="count">'+str(new_sub_dict[item])

					if diff_dict != None:
						diff = diff_dict[category][item]
						if diff < 0:
							text += ' ('+str(diff)+')'
						elif diff > 0:
							text += ' (+'+str(diff)+')'

					text += '</td></tr>'

				cat = category+"_"+str(i+1)

				text_dict[cat] = text

	#place all generated text into html string
	template = template.replace('[INSERT BANNER]', banner)
	template = template.replace('[INSERT LOGO]', logo)
	template = template.replace('[INSERT TITLE]', name)
	template = template.replace('[INSERT STAGE ENTRIES]', text_dict['stages'])
	template = template.replace('[INSERT MEMBER TYPE ENTRIES]', text_dict['member_types'])
	template = template.replace('[INSERT INTEREST 1 ENTRIES]', text_dict['interests_1'])
	template = template.replace('[INSERT INTEREST 2 ENTRIES]', text_dict['interests_2'])
	template = template.replace('[INSERT LOCATION 1 ENTRIES]', text_dict['locations_1'])
	template = template.replace('[INSERT LOCATION 2 ENTRIES]', text_dict['locations_2'])
	template = template.replace('[INSERT LOCATION 3 ENTRIES]', text_dict['locations_3'])
	template = template.replace('[INSERT LOCATION 4 ENTRIES]', text_dict['locations_4'])
	template = template.replace('[INSERT EXPERTISE 1 ENTRIES]', text_dict['expertises_1'])
	template = template.replace('[INSERT EXPERTISE 2 ENTRIES]', text_dict['expertises_2'])
	template = template.replace('[INSERT INDUSTRY 1 ENTRIES]', text_dict['industries_1'])
	template = template.replace('[INSERT INDUSTRY 2 ENTRIES]', text_dict['industries_2'])
	template = template.replace('[INSERT NUM USERS]', size)
	template = template.replace('[INSERT PERCENT ACTIVE]', active)
	template = template.replace('[INSERT CURRENT DATE]', date)
	template = template.replace('[INSERT PREVIOUS DATE]', prev_date)

	return template #return filled html string


def generate_reports(curr_directory, prev_directory, sum_dict, diff_sum_dict, group_dicts, diff_group_dict):
	#parent function that generates sum and group reports
	
	curr_date = get_curr_date()

	html = generate_html(curr_directory, prev_directory, sum_dict, diff_sum_dict, "sum") #get html string for sum report

	file_name = "Sum_User_Report" #name for sum report
	path = './reports/'+curr_date+'/'
	generate_pdf(html, None, file_name, path) #generate pdf from sum html string

	for group in curr_directory.groups: #repeat above process for all groups
		gid = group.gid
		group_dict = group_dicts[gid]
		diff_dict = diff_group_dict[gid]

		html = generate_html(curr_directory,prev_directory, group_dict, diff_dict, gid) #generate html string for single group

		file_name = group.name
		path = './reports/'+curr_date+'/Group_Reports/'

		generate_pdf(html, gid, file_name, path) #generate pdf from html string for group


def fetch_directories():
	#Function used to create directories with stored user and group objects

	export_dir_name = "./data/user_exports/"
	dates = get_dates(export_dir_name) #gets sorted dates for exports saved

	curr_date = format_date(dates[0]) #saves and formatts most current date
	prev_date = None #default value of next current date
	if len(dates) > 1: #if there are multiple exports saved...
		prev_date = format_date(dates[1]) #gets and formats next recent date

	export_name = "User_export_" + dates[0] + ".xlsx"
	export_path = export_dir_name + export_name

	curr_directory = Directory() #create directory object
	curr_directory.current_date = curr_date #save date of directory
	curr_directory.group_names = read_group_names("./data/group_data/") #get group names for directory
	curr_directory.users = read_users(export_path, curr_directory) #get users for directory
	curr_directory.users.sort(key=lambda user:user.score, reverse=True) #sort users based off activity score

	prev_directory = None #default value of directory

	if prev_date != None: #prev directory only created if another date exists (more than one export exists)
		export_name = "User_export_" + dates[1] + ".xlsx"
		export_path = export_dir_name + export_name

		#same process as curr_directory, but for previous date/export
		prev_directory = Directory()
		prev_directory.current_date = prev_date
		prev_directory.group_names = read_group_names("./data/group_data/")
		prev_directory.users = read_users(export_path, prev_directory)
		prev_directory.users.sort(key=lambda user:user.score, reverse=True)

	return curr_directory, prev_directory


#======================================
# DICTIONARY HANDLER FUNCTIONS
#======================================
def create_dict(data):
	#creates dictionary of users in data object (either directory or group object)

	data_dict = {} #parent dict

	locations = {} #sub dict for lacations
	industries = {}
	expertises = {}
	interests = {}
	resources = {}
	stages = {}
	member_types = {}

	for industry in _desired_content.industries:
		industries[industry] = 0
	for expertise in _desired_content.expertise:
		expertises[expertise] = 0
	for interest in _desired_content.interests:
		interests[interest] = 0

	for user in data.users: #iterate over every user

		if user.active: #only record stats for active users
		
			location = user.location.split(",")[0] 
			if location not in locations:
				locations[location] = 1
			else:
				locations[location] += 1
				
			for industry in user.categories['industry']:
				if industry not in _desired_content.industries:
					continue
				else:
					industries[industry] += 1
			
			for expertise in user.categories['expertise']:
				if "Financial" in expertise:
					expertise = "Financial"
				if expertise not in _desired_content.expertise:
					continue
				else:
					expertises[expertise] += 1

			for interest in user.categories['interests']:
				if "Financial" in interest:
					interest = "Financial"
				if interest not in _desired_content.interests:
					continue
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
	
	#sort and store all sub-dictionaries into parent dictionary that will be returned
	data_dict["locations"] = dict(sorted(locations.items(), key=lambda item:item[1], reverse=True))
	data_dict["industries"] = dict(sorted(industries.items(), key=lambda item:item[1], reverse=True))
	data_dict["expertises"] = dict(sorted(expertises.items(), key=lambda item:item[1], reverse=True))
	data_dict["interests"] = dict(sorted(interests.items(), key=lambda item:item[1], reverse=True))
	data_dict["resources"] = dict(sorted(resources.items(), key=lambda item:item[1], reverse=True))
	data_dict["stages"] = dict(sorted(stages.items(), key=lambda item:item[1], reverse=True))
	data_dict["member_types"] = dict(sorted(member_types.items(), key=lambda item:item[1], reverse=True))
	return data_dict #return parent dict


def fetch_dicts(directory):
	#function returns both sum and group dictionaries for a given directory

	sum_dict = None #default value of dict
	group_dict = None 

	if directory != None: #if a directory exists and has been initialized
		sum_dict = create_dict(directory) #create sum dictionary
		group_dict = {}
		for group in directory.groups: #repeat same process for all groups
			group_dict[group.gid] = create_dict(group)

	return sum_dict, group_dict


def create_diff_dict(curr_dict, prev_dict):
	#creates a dictionary that highlights differences in current directory and previous directory from user export
	#used in pdf reports to show how userbase has changed

	diff_dict = {}

	for category in curr_dict.keys(): #iterate over all keys
		category_dict = {}
		for item in curr_dict[category].keys(): #iterate over all values in dict
			diff = 0 #default value of difference
			if item in prev_dict[category]: #check item exists in prev dict and get difference
				diff = curr_dict[category][item] - prev_dict[category][item] 
			else: #if item doesn't exist, difference is just the current count in current dictionary
				diff = curr_dict[category][item]

			category_dict[item] = diff #save result
		diff_dict[category] = category_dict #save sub dictionary

	return diff_dict #return final difference dict


def fetch_diff_dicts(directory, curr_group_dict, curr_sum_dict, prev_group_dict, prev_sum_dict):
	#returns diff dictionaries of group and sum dictionaries bassed off differences of data

	diff_sum_dict = None #default value
	diff_group_dict = None

	if prev_sum_dict != None and prev_group_dict != None: #only create diff dicts if previous dicts exists 
		
		diff_sum_dict = create_diff_dict(curr_sum_dict, prev_sum_dict) #create diff dict for sum report
		diff_group_dict = {} #initialize diff group dict

		for group in directory.groups: #get diff dict for each group
			gid = group.gid

			curr_dict = curr_group_dict[gid]
			prev_dict = curr_dict
			if gid in prev_group_dict: #check if group exists in previous export
				prev_dict = prev_group_dict[gid]

			diff_group_dict[group.gid] = create_diff_dict(curr_dict, prev_dict) #get diff dict for group

	return diff_sum_dict, diff_group_dict


#======================================
# ERROR CHECK FUNCTIONS
#======================================
def check_reports():
	#error check function that deletes all previously created pdf reports
	#tells user to close any pdf report open and returns error if one IS open

	error = False

	curr_date = get_curr_date()

	sum_path = './reports/'+curr_date
	group_path = './reports/'+curr_date+'/Group_Reports'

	try:
		os.mkdir('./reports') #create report folder if it does not exist
	except OSError as e:
		pass #do not report error if folders already exist
	try:
		os.mkdir(sum_path)
	except OSError as e:
		pass #do not report error if folders already exist
	try:
		os.mkdir(group_path) #create group report folder if it does not exist
	except OSError as e:
		pass #do not report error if folders already exist


	paths = ['./reports/'+curr_date+'/', './reports/'+curr_date+'/Group_Reports/'] #paths to delete pdfs from

	for path in paths:
		files = [f for f in listdir(path) if isfile(join(path, f))]	#get all files in path
		for file in files:
			try:
				os.remove(path+file) #try to remove pdf file from folder
			except OSError as e:
				print ("ERROR: CLOSE ALL OPEN PDF REPORTS!") #report to user that pdf is open and needs to be closed
				error = True #save that error exists
			if error: #break loop if error exists
				break
		if error:#break loop if error exists
			break

	return error


def check_dates():
	#checks that user export files exist
	#returns an error if NO export files are found

	error = False
	try:
		path = "./data/user_exports/" #path to look for exports
		dates = get_dates(path) #gets dates of files found

		if len(dates) == 0: #if no files are found
			print("ERROR: NO USER EXPORTS FOUND IN DATA FOLDER") #report error
			error = True

	except OSError as e:
		print("ERROR: path 'data/user_exports/' not found. To ensure full functionality of code, re-copy original 'data' folder from .zip file and place it back in 'user_reports' main folder.")

	return error


def check_groups():
	#checks that all group names and ids are saved in appropriate file in data folder
	#if all groups are not saved correctly, reports error

	error = False

	export_dir_name = "./data/user_exports/"

	dates = get_dates(export_dir_name)
	curr_date = dates[0]
	curr_date = format_date(curr_date)

	export_name = "User_export_" + dates[0] + ".xlsx"
	export_path = export_dir_name + export_name
	group_dir_name = "./data/group_data/"

	df = pd.read_excel(export_path) #get data from user export
	df = df.fillna("") #fills empty entries with empty strings

	categories = list(df.columns) #gets all categories from file
	data = df.to_numpy() #converts dataframe to an array

	index = get_index(categories, "Groups Member:Group Member") #gets index of desired data field from export data

	all_groups = []
	for row in data: #loop gets all groups currently in the user export
		groups = fix_list(row[index].split(","))
		for group in groups:
			if group not in all_groups:
				all_groups.append(group)

	saved_groups = read_group_names("./data/group_data/") #loads all saved groups into a dictionary

	for gid in all_groups: #check that all groups in current export exist in saved group name file
		if int(gid) not in saved_groups: #if group exists in current export but not in saved name file
			print("ERROR: ***GROUP "+gid+"*** NAME NOT SAVED!") #throw error
			print("ENSURE ALL GROUP NAMES AND ID'S ARE SAVED IN 'data/group_data/names.csv'!")
			error = True #report error
			break

	return error


main()