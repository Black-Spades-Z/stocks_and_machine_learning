from flask_mysqldb import MySQL
from flask_login import UserMixin
from werkzeug.security import check_password_hash


mysql = MySQL()


# Example user class (adjust based on your Users table structure)
class User(UserMixin):
    def __init__(self, user_id, email, password_hash, full_name, income):
        self.id = user_id
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.income = income

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def init_app(app):
    mysql.init_app(app)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'zero'
    app.config['MYSQL_PASSWORD'] = 'zero'
    app.config['MYSQL_DB'] = 'Stocks'


def check_user(email):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT Email FROM Users WHERE Email LIKE "{email}"')
        data = cur.fetchall()
        cur.close()
        print(data)
        if data == email:
            print("There is a user")

            return False
        return True
    except Exception :
        print(Exception)
    return False

def register_user(email, password, fullName):
    try:

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Users(Email, Password, FullName, Income) VALUES(%s, %s, %s, 0);', (email, password, fullName))
        mysql.connection.commit()
        cur.close()
        print("Success")
        return True
    except Exception as e :
        print(e)
        return False


def get_user_by_id(email):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT * FROM Users WHERE Email LIKE "{email}"')
        user_data = cur.fetchall()
        cur.close()
        print(user_data[0])
        user_data = list(user_data[0])
        if user_data[1] == email:
            print("There is a user")
            return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    except Exception:
        print(Exception)
    return User
