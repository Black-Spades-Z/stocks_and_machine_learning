from flask import Blueprint, render_template, request, session, url_for, redirect, flash, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from database_management import check_user, register_user, User, get_user_by_id

views = Blueprint(__name__,'views')
login_manager = LoginManager()
def init_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to log in to access this page.')
    return redirect(url_for('views.loginIn'))




@views.route('/login',  methods=('GET', 'POST'))
def loginIn():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = load_user(email)
        if user.check_password(password):
            login_user(user)
            print(f'User {email} logged in successfully')
            return redirect(url_for("views.main_page"))
        else:
            return 'Invalid Password'



@views.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not name:
            error = 'Name is required.'
        elif not surname:
            error = 'Surname is required.'
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                if check_user(email):
                    # Hash the password
                    password_hash = generate_password_hash(password)

                    fullName = name + " " + surname
                    if register_user(email, password_hash, fullName):
                        print("Registered and Redirecting")
                        user = load_user(email)
                        login_user(user)
                        return redirect(url_for("views.main_page"))

            except Exception:
                error = f"User {email} is already registered."
        else:

            return 'redirect(url_for("views.loginIn"))'

        flash(error)

    return redirect(url_for("views.loginIn"))

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully'

@views.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.full_name}! Welcome to the dashboard'

@views.route('/')
@login_required
def main_page():
    return render_template("index.html")

@views.route('/items/<stock>')
@login_required
def stock_info(stock):
    return render_template("stock_page.html", stock_name= stock)

