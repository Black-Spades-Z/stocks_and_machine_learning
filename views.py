from flask import Blueprint, render_template, request, session, url_for, redirect, flash, g
from werkzeug.security import check_password_hash, generate_password_hash

from database_management import check_user

views = Blueprint(__name__,'views')

@views.route('/login')
def loginIn():
    check_user("cruschkarsten7@gmail.com")
    return render_template("login.html")

@views.route('/')
def main_page():
    return render_template("index.html")

@views.route('/items/<stock>')
def stock_info(stock):
    return render_template("stock_page.html", stock_name= stock)



# @views.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         error = None
#
#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'
#
#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))
#
#         flash(error)
#
#     return render_template('auth/register.html')