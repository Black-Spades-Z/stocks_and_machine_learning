from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import datetime
import os


app = Flask(__name__)
CORS(app)  # Initialize CORS with default settings|

# Database initialization

db_user = 'zero'
db_password = 'zero'
db_host = 'localhost'
db_port = '3306'
db_name = 'Stocks'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


db = SQLAlchemy(app)
# JWT configuration
app.config['JWT_SECRET_KEY'] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6b78b7a49acae9"  # Change this to a strong secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
jwt = JWTManager(app)



class User(db.Model):
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





@jwt.unauthorized_loader
def unauthorized_callback(error):
    return redirect(url_for('login')), 401

@app.route('/')
@jwt_required()
def index():
    return redirect(url_for('main_page'))

@app.route('/main-page')
@jwt_required()
def main_page():
    print("I am working")
    print(request.path)
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
            return jsonify({"message": "Invalid email or password"})

        # Create access and refresh tokens
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        return jsonify({"message": "success", "access_token": access_token, "refresh_token": refresh_token}), 200
    return "Not allowed method", 404


# Token refresh endpoint
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200




with app.app_context():
    create_db_and_tables()





if __name__ == '__main__':
    app.run(debug=True, port=5000)










