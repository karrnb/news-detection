#!/usr/bin/python
import MySQLdb
import csv

if __name__ == '__main__':
    db = MySQLdb.connect(host="localhost",  # your host
                         user="cs512",  # username
                         passwd="cs512password",  # password
                         db="news_classifier")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # f = open("NewsAggregatorDataset/newsCorpora.csv")
    f = open("newsCorpora.csv")
    csv_data = csv.reader(f,delimiter='\t')

    cur.execute("DELETE FROM dataset")
    cur.execute("ALTER TABLE dataset AUTO_INCREMENT = 1")
    db.commit()

    for index,row in enumerate(csv_data):

        query="INSERT INTO dataset (text, category) values (%s, %s)"
        try:
            cur.execute(query, (row[1], row[4]))
        except:
            pass
        if index%10000==0:
            print index
            db.commit()

    db.commit()

    #Get column names from table
    cur.execute("SHOW columns FROM dataset")
    print [column[0] for column in cur.fetchall()]

    print "Done"

    cur.close()
