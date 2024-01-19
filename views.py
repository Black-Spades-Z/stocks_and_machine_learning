from flask import Blueprint, render_template


views = Blueprint(__name__,'views')

@views.route('/')
def main_page():
    return render_template("index.html")

@views.route('/<stock>')
def stock_info(stock):
    return render_template("stock_page.html", stock_name= stock)