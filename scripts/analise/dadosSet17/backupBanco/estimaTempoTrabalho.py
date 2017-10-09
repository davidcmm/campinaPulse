#Script to estimate mean and median worktime of each user in Como e Campina
import sys
import time as tm
import datetime
from sets import Set
import json
import numpy as np

def readUserData(lines1, lines2, outputFileName):
	""" Reading user profile """
	
	users_tasks = {}
	users_tasks_diff = {}
	firstDate = datetime.date(1970, 6, 24)
	agrad_dic = {"agradavel?" : "agrad%C3%A1vel?", "agrad%C3%A1vel?" : "agradavel?"}

	#Reading from pybossa task-run CSV - V1
	for line in lines1:
		data = line.split("+")
	
		created = data[1].split("T")[0].split("-")
		created.extend(data[1].split("T")[1].split(":"))
		created.extend(created[5].split("."))
		task_id = data[3]
		user_id = data[4]
		time_info = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		time_info.extend(data[6].split("T")[1].split(":"))
		time_info.extend(time_info[5].split("."))
		init_time = datetime.datetime(int(created[0]), int(created[1]), int(created[2]), int(created[3]), int(created[4]), int(created[6]), int(created[7]))
		finish_time = datetime.datetime(int(time_info[0]), int(time_info[1]), int(time_info[2]), int(time_info[3]), int(time_info[4]), int(time_info[6]), int(time_info[7]))

		if user_id in users_tasks.keys():
			user_worktimes = users_tasks[user_id]
			user_worktimes_diff = users_tasks_diff[user_id]
		else:
			user_worktimes = []
			user_worktimes_diff = []
		user_worktimes.append((finish_time - init_time).total_seconds())
		user_worktimes_diff.append(finish_time)

		users_tasks[user_id] = user_worktimes
		users_tasks_diff[user_id] = user_worktimes_diff

	#Reading from pybossa task-run CSV - V2
	for line in lines2:
		data = line.split("+")

		created = data[1].split("T")[0].split("-")
		created.extend(data[1].split("T")[1].split(":"))
		created.extend(created[5].split("."))
		task_id = data[3]
		user_id = data[4]
		time_info = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		time_info.extend(data[6].split("T")[1].split(":"))
		time_info.extend(time_info[5].split("."))
		init_time = datetime.datetime(int(created[0]), int(created[1]), int(created[2]), int(created[3]), int(created[4]), int(created[6]), int(created[7]))
		finish_time = datetime.datetime(int(time_info[0]), int(time_info[1]), int(time_info[2]), int(time_info[3]), int(time_info[4]), int(time_info[6]), int(time_info[7]))

		if user_id in users_tasks.keys():
			user_worktimes = users_tasks[user_id]
			user_worktimes_diff = users_tasks_diff[user_id]
		else:
			user_worktimes = []
			user_worktimes_diff = []
		user_worktimes.append((finish_time - init_time).total_seconds())
		user_worktimes_diff.append(finish_time)

		users_tasks[user_id] = user_worktimes
		users_tasks_diff[user_id] = user_worktimes_diff

	#Computing average worktime per user
	for user_id in users_tasks.keys():
		user_worktimes = users_tasks[user_id]
		user_worktimes_diff = users_tasks_diff[user_id]

		current_diffs = []
		for index in range(1, len(user_worktimes_diff)):
			time1 = user_worktimes_diff[index-1]
			time2 = user_worktimes_diff[index]

			if time1 > time2:
				greater = time1
				lower = time2
			else:
				greater = time2
				lower = time1
			worktime = (greater - lower).total_seconds()
			if worktime <= 5 * 60:
				current_diffs.append(worktime)

		#if user_id == "617":
		#	for value in user_worktimes:
		#		print "work\t" + str(value)
		#	for value in current_diffs:
		#		print "diff\t" + str(value)
		print user_id + "\t" + str(np.mean(user_worktimes)) + "\t" + str(np.median(user_worktimes)) + "\t" + str(np.sum(user_worktimes)) + "\t" + str(np.mean(current_diffs)) + "\t" + str(np.median(current_diffs)) + "\t" + str(np.sum(current_diffs))


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios - V1> <arquivo com execucoes das tarefas e perfis dos usuarios - V2>"
		sys.exit(1)

	dataFile1 = open(sys.argv[1], 'r')
	dataFile2 = open(sys.argv[2], 'r')
	
	lines1 = dataFile1.readlines()
	lines2 = dataFile2.readlines()

	usersTasks = readUserData(lines1, lines2, "worktime.dat")
	dataFile1.close()
	dataFile2.close()
