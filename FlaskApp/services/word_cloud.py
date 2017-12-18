from . import services
import MySQLdb
from app import app
from numpy import genfromtxt

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

def generate_words(classifier):
    mysql_obj_classifier = mysql_connection('news_classifier')
    query = 'select class,word,sum(count) as sum_count from WORD_CLASS_COUNTS where class=\"' + classifier + '\" group by class,word order by sum_count desc limit 50;'
    class_info = []
    mysql_obj_classifier.execute_query(query)
    # class_info = {row[1]:{"count":row[2]} for row in mysql_obj_classifier.cursor.fetchall()}
    for row in mysql_obj_classifier.cursor.fetchall():
        class_info.append({"text": row[1], "weight": int(row[2])})
    return class_info


def generate_cloud(classifier):
    omit_words = ['...', 'after', 'although', 'and', 'as', 'because', 'before', 'but', 'for', 'how', 'if', 'lest', 'nor', 'now that', 'once', 'or', 'since', 'so', 'to', 'than', 'that', 'though', 'till', 'unless', 'until', 'when', 'whenever', 'where', 'whereas', 'wherever', 'whether', 'while', 'yet', 'the', 'of', 'and', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will','us', 'now', 'one','up', 'can', 'could', 'says', '1', '2']
    # omit_words = genfromtxt('words.txt', delimiter='\n')
    weight_mapping = generate_words(classifier)
    weight_mapping_clean = []
    for row in weight_mapping:
        if row["text"] not in omit_words:
            weight_mapping_clean.append(row)
    return weight_mapping_clean
