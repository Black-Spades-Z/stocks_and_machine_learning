from flask_mysqldb import MySQL




mysql = MySQL()
def init_app(app):
    mysql.init_app(app)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'zero'
    app.config['MYSQL_PASSWORD'] = 'zero'
    app.config['MYSQL_DB'] = 'Stocks'


def check_user(email):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT * FROM Users WHERE Email LIKE "{email}"')
        data = cur.fetchall()
        cur.close()
        print("Success")
        print(data)
    except Exception :
        print(Exception)
