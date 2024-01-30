from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_cors import CORS
import datetime
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecretkey'
app.permanent_session_lifetime = datetime.timedelta(minutes=30)
CORS(app)  # Initialize CORS with default settings|


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database initialization

db_user = 'zero'
db_password = 'zero'
db_host = 'localhost'
db_port = '3306'
db_name = 'Stocks'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f'<User : {self.email} >'



# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Utility functions
def hash_password(password):
    return pwd_context.hash(password)


# Database Initialization
def create_db_and_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('401.html'), 404

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    print("Unauthorized User")
    return render_template('401.html'), 401

@app.route('/')
@login_required
def main_page():
    return render_template("index.html")



# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    name = data.get('name')
    surname = data.get('surname')
    password = data.get('password')
    full_name = name + " " + surname

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already registered"})

    hashed_password = hash_password(password)
    new_user = User( email=email, hashed_password=hashed_password, full_name=full_name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User successfully registered"}), 201

# User Login Endpoint
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not pwd_context.verify(password, user.hashed_password):
            return jsonify({"message": "Invalid email or password"}), 401
        login_user(user)
        session.permanent = True
        return redirect(url_for('main_page')), 200
    return "Not allowed method", 404


# Token refresh endpoint
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))



with app.app_context():
    create_db_and_tables()





if __name__ == '__main__':
    app.run(debug=True, port=5000)










