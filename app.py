from flask import Flask, render_template

from database_management import init_app
from views import views, init_login

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.debug = True


app.register_blueprint(views, url_prefix='/')
init_app(app)
init_login(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, port=6969)
