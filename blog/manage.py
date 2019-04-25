
from flask import Flask
from flask_script import Manager

from back.models import db
from back.views import blue
from web.views import blue2

app =Flask(__name__)

app.register_blueprint(blueprint=blue,url_prefix='/back')
app.register_blueprint(blueprint=blue2,url_prefix='/')

app.config['SECRET_KEY'] = 'wojiushiwoshiyansebuyiyangdeyanhuo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhang1997@localhost:3306/blogdb'

db.init_app(app)

if __name__ == '__main__':
    manage = Manager(app)
    manage.run()