from . import services
from flask_mysqldb import MySQL
import MySQLdb
from app import app
from collections import defaultdict
import random
import numpy as np
import re
import operator
import math
import sys

class mysql_connection(object):
    def __init__(self,db):
        self.db = MySQLdb.connect(host = app.config['MYSQL_HOST'],
                             user = app.config['MYSQL_USER'],
                             passwd = app.config['MYSQL_PASSWORD'],
                             db=db)  # name of the database
        self.cursor = self.db.cursor()

    def execute_query(self, query, commit=True):
        self.cursor.execute(query)
        if commit==True:
            self.db.commit()

    def commit(self):
        self.db.commit()

def test():
    return "Testing"

def test2(inputs, mysql_obj):
    mysql_obj.execute_query("SELECT CLASS, COUNT, PRIOR from CLASS_COUNTS_PRIORS")
    class_info = {row[0]:{"count":row[1], "prior":row[2]} for row in mysql_obj.cursor.fetchall()}
    labels = []
    mysql_obj.execute_query("select count(distinct(word)) from WORD_CLASS_COUNTS")
    vocabulary_size = int(mysql_obj.cursor.fetchall()[0][0])
    for i in range(len(inputs)):
        input = normalize_text(inputs[i])
        input_tokens = input.split()
        class_prob = {}
        for cl, cl_info in class_info.items():
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
        labels.append(max(class_prob.items(), key=operator.itemgetter(1))[0])
    return labels

# def execute_query(db_name, query):
#     app.config['MYSQL_DB'] = db_name
#     app.config.from_object('config')
#     mysql = MySQL(app)
#     mysql.init_app(app)
#     print(app.config['MYSQL_DB'])
#     print(query)
#     cur = mysql.connection.cursor()
#     cur.execute(query)
#     mysql.connection.commit()
#     # rv = cur.fetchall()
#     # print(rv)
#     return cur

# def test(inputs, mysql_db):
#     # mysql_obj.execute_query("SELECT CLASS, COUNT, PRIOR from CLASS_COUNTS_PRIORS")
#     cur = execute_query(mysql_db, "SELECT CLASS, COUNT, PRIOR from CLASS_COUNTS_PRIORS")
#     class_info = {row[0]:{"count":row[1], "prior":row[2]} for row in cur.fetchall()}
#     # print(mysql_db)
#     # print(class_info)
#     cur.close()
#     labels = []
#     cur = execute_query(mysql_db, "select count(distinct(word)) from WORD_CLASS_COUNTS")
#     vocabulary_size = int(cur.fetchall()[0][0])
#     cur.close()
#     for i in range(len(inputs)):
#         input = normalize_text(inputs[i])
#         input_tokens = input.split()
#         class_prob = {}
#         for cl, cl_info in class_info.items():
#             class_prob[cl] = math.log(cl_info['prior'])
#             for token in input_tokens:
#                 try:
#                     cur = execute_query(mysql_db, "SELECT COUNT from WORD_CLASS_COUNTS WHERE WORD='%s' AND CLASS='%s'" %(token.replace("'","''"),cl))
#                     count_arr = [row[0] for row in cur.fetchall()]
#                     cur.close()
#                     if len(count_arr)==0:
#                         count_arr = [0]
#                 except:
#                     count_arr = [0]
#                 class_prob[cl] += math.log((count_arr[0]+1)/(float(cl_info['count']+vocabulary_size)))
#                 print(class_prob)
#         labels.append(max(class_prob.items(), key=operator.itemgetter(1))[0])
#         # print(labels)
#     return labels

def normalize_text(text):
    text = text.lower()
    # remove punctuation except word-internal (hyphens, apostrophes)
    text = re.sub('\s\W',' ', text)
    text = re.sub('\W\s',' ', text)
    # removing double spaces
    text = re.sub('\s+',' ', text)
    return text

def check_text(input_text):
    # input_text = 'new jerry seinfeld show releases'
    mysql_obj_identifier = mysql_connection('news_identifier')
    mysql_obj_classifier = mysql_connection('news_classifier')
    input_text = normalize_text(input_text)
    identifier_output = test2([input_text], mysql_obj_identifier)
    if identifier_output[0] == 'news':
        # identifier_output[0] = 'News'
        classifier_output = test2([input_text], mysql_obj_classifier)
        print(classifier_output)
    else:
        # identifier_output[0] = 'Not News'
        classifier_output = []
    print(identifier_output)
    return identifier_output, classifier_output
