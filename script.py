import csv
import operator

# I think it’d be helpful to create views sorted by engagement score, resources, and date created (descending).
# Eventually we’ll want to create user lists for group moderators to send targeted email campaigns to.
# Those will likely start on a case by case basis, so I’ll let you know when we have a request.


class User:
	def __init__(self, uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests):
		self.uid = uid #user id
		self.first_name = first_name #tracks name of play
		self.last_name = last_name
		self.email = email
		self.last_active = last_active
		self.created = created
		self.count = count
		self.score = score
		self.groups = [] #tracks groups person is associated with
		self.expertise = []
		self.industry = []
		self.interests = []

def fix_list(list):
	result = []
	for item in list:
		if item != '':
			if item[0] == ' ':
				item = item[1:]
			result.append(item)
	return result


def main():

	users = []

	with open('data/user_export.csv', newline='') as csvfile:
		file = csv.reader(csvfile, delimiter=',')
		i = 0
		index_cat = False
		for row in file:
			if i == 0:
				if index_cat:
					k = 0
					for item in row:
						print(str(k)+":"+item)
						k += 1
			else:
				uid = row[0]
				first_name = row[7]
				last_name = row[4]
				email = row[10]
				last_active = row[41]
				created = row[44]
				count = row[40]
				score = row[119]
				groups = fix_list(row[117].split(","))
				expertise = fix_list(row[124].split(","))
				industry = fix_list(row[128].split(","))
				interests = fix_list(row[130].split(","))
				
				user = User(uid, first_name, last_name, email, last_active, created, count, score, groups, expertise, industry, interests)
				users.append(user)
			i += 1

	print(len(users))

	with open("./results.csv", "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		string = ""
		writer.writerow([string])


main()