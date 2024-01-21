from flask import Flask

from database_management import init_app
from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix='/')
init_app(app)


if __name__ == '__main__':
    app.run(debug=True, port=6969)
