#Dataset source:
#https://archive.ics.uci.edu/ml/datasets/News+Aggregator

from collections import defaultdict
import random
import numpy as np
import re
import MySQLdb
import operator
import math
import sys


__author__ = 'ankush'

class mysql_connection(object):
	def __init__(self,db):
		self.db = MySQLdb.connect(host="localhost",  # your host
							 user="cs512",  # username
							 passwd="cs512password",  # password
							 db=db)  # name of the database
		self.cursor = self.db.cursor()

	def execute_query(self, query, commit=True):
		self.cursor.execute(query)
		if commit==True:
			self.db.commit()

	def commit(self):
		self.db.commit()


def normalize_text(text):
	text = text.lower()

	# remove punctuation except word-internal (hyphens, apostrophes)
	text = re.sub('\s\W',' ', text)
	text = re.sub('\W\s',' ', text)

	# removing double spaces
	text = re.sub('\s+',' ', text)

	return text


def get_dataset_size(mysql_obj):
	mysql_obj.execute_query("SELECT COUNT(*) FROM DATASET")
	size = int(mysql_obj.cursor.fetchall()[0][0])
	return size


def get_dataset_classes(mysql_obj):
	mysql_obj.execute_query("SELECT DISTINCT CATEGORY FROM DATASET")
	rows = mysql_obj.cursor.fetchall()
	classes = []
	for row in rows:
		classes.append(row[0])
	return classes


def init_class_priors(classes, mysql_obj):
	num_classes = len(classes)
	dataset_size = get_dataset_size(mysql_obj)
	for cl in classes:
		mysql_obj.execute_query("SELECT COUNT(*) FROM DATASET WHERE category='%s'" %(cl))
		class_size = int(mysql_obj.cursor.fetchall()[0][0])
		prior = class_size/float(dataset_size)
		query = "INSERT INTO CLASS_COUNTS_PRIORS(class,count,prior) VALUES('%s', 0, %f) ON DUPLICATE KEY UPDATE prior=%f;" %(cl, prior, prior)
		mysql_obj.execute_query(query)
	mysql_obj.commit()


def train(inputs, labels, mysql_obj):
	for i in range(len(inputs)):
		label = labels[i]
		input = normalize_text(inputs[i])
		input_tokens = input.split()
		for token in input_tokens:
			query = "INSERT INTO WORD_CLASS_COUNTS VALUES('%s','%s',1) ON DUPLICATE KEY UPDATE count=count+1" %(token.replace("'","''"), label)
			try:
				mysql_obj.execute_query(query)
			except:
				pass
		num_tokens = len(input_tokens)
		query = "INSERT INTO CLASS_COUNTS_PRIORS(class,count) VALUES('%s',%d) ON DUPLICATE KEY UPDATE count=count+%d" %(label, num_tokens, num_tokens)
		mysql_obj.execute_query(query)
	mysql_obj.commit()


def test(inputs, mysql_obj):
	mysql_obj.execute_query("SELECT CLASS, COUNT, PRIOR from CLASS_COUNTS_PRIORS")
	class_info = {row[0]:{"count":row[1], "prior":row[2]} for row in mysql_obj.cursor.fetchall()}
	labels = []
	mysql_obj.execute_query("select count(distinct(word)) from WORD_CLASS_COUNTS")
	vocabulary_size = int(mysql_obj.cursor.fetchall()[0][0])
	for i in range(len(inputs)):
		input = normalize_text(inputs[i])
		input_tokens = input.split()
		class_prob = {}
		for cl, cl_info in class_info.iteritems():
			# print cl, cl_info
			class_prob[cl] = math.log(cl_info['prior'])
			for token in input_tokens:
				try:
					mysql_obj.execute_query("SELECT COUNT from WORD_CLASS_COUNTS WHERE WORD='%s' AND CLASS='%s'" %(token.replace("'","''"),cl))
					count_arr = [row[0] for row in mysql_obj.cursor.fetchall()]
					if len(count_arr)==0:
						count_arr = [0]
				except:
					count_arr = [0]
				class_prob[cl] += math.log((count_arr[0]+1)/(float(cl_info['count']+vocabulary_size)))
			# 	print token, count_arr[0]
			# print
		# sum_prob = np.sum(class_prob.values())
		# for cl, prob in class_prob.iteritems():
		# 	class_prob[cl] = prob/sum_prob
		# print input
		# print class_prob
		# print
		labels.append(max(class_prob.iteritems(), key=operator.itemgetter(1))[0])
	return labels


def clear_word_class_counts_table(mysql_obj):
	mysql_obj.execute_query("DELETE FROM WORD_CLASS_COUNTS")
	mysql_obj.commit()


def clear_class_counts(mysql_obj):
	mysql_obj.execute_query("UPDATE CLASS_COUNTS_PRIORS SET COUNT=0")
	mysql_obj.commit()

if __name__ == '__main__':
	mysql_obj = mysql_connection(sys.argv[1])
	mysql_obj.commit()

	init_class_priors(get_dataset_classes(mysql_obj), mysql_obj)

	dataset_size = get_dataset_size(mysql_obj)
	test_indices = set(random.sample(range(1, dataset_size), int(0.2*dataset_size)))
	# test_indices = set(random.sample(range(1, 150000), 15000))
	test_inputs = []
	test_labels = []

	clear_word_class_counts_table(mysql_obj)
	clear_class_counts(mysql_obj)

	start = 0
	step = 1000
	while start <= dataset_size:
		print start
		# if start==150000:
		# 	break
		mysql_obj.execute_query("SELECT id,text, category FROM DATASET ORDER BY ID LIMIT %d,1000" %(start))
		rows = mysql_obj.cursor.fetchall()
		train_inputs = []
		train_labels = []
		for row in rows:
			id = int(row[0])
			if id in test_indices:
				test_inputs.append(row[1])
				test_labels.append(row[2])
			else:
				train_inputs.append(row[1])
				train_labels.append(row[2])
		train(train_inputs, train_labels, mysql_obj)
		start += step

	output_labels = test(test_inputs, mysql_obj)

	accurate_count = 0
	for index, label in enumerate(output_labels):
		if label==test_labels[index]:
			accurate_count += 1

	print accurate_count/float(len(output_labels))
