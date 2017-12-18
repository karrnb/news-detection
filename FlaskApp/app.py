from flask import Flask
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from werkzeug import generate_password_hash, check_password_hash
from routes import *

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(routes)
# mysql = MySQL(app)
Bootstrap(app)


@app.route("/")
def connection():
    # db = mysql.connection(MYSQL_HOST = app.config['MYSQL_DATABASE_HOST'],
    #                       MYSQL_USER = app.config['MYSQL_DATABASE_USER'],
    #                       MYSQL_PASSWORD = app.config['MYSQL_DATABASE_PASSWORD'],
    #                       MYSQL_DB = app.config['MYSQL_DATABASE_DB'])
    # cur = db.cursor()
    # cur.execute("SELECT * FROM DATASET")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM DATASET")
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'],
            port=app.config['PORT'])
