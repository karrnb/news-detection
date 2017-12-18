#!/usr/bin/python
import MySQLdb
import csv

def populate(f,csv_data,db,cur,cat):
    for index,row in enumerate(csv_data):
        query="INSERT INTO dataset (text, category) values (%s, %s)"
        try:
            cur.execute(query, (row[2], cat))
        except Exception,e:
            # print repr(e)
            pass
        if index%10000==0:
            print index
            db.commit()
    db.commit()


if __name__ == '__main__':
    db = MySQLdb.connect(host="localhost",  # your host
                         user="cs512",  # username
                         passwd="cs512password",  # password
                         db="news_identifier")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    cur.execute("DELETE FROM dataset")
    cur.execute("ALTER TABLE dataset AUTO_INCREMENT = 1")
    db.commit()

    f = open("news_tweets.csv")
    csv_data = csv.reader(f)
    populate(f,csv_data,db,cur,'news')

    f = open("non_news_tweets.csv")
    csv_data = csv.reader(f)
    populate(f,csv_data,db,cur,'not_news')

    #Get column names from table
    cur.execute("SHOW columns FROM dataset")
    print [column[0] for column in cur.fetchall()]

    print "Done"

    cur.close()
