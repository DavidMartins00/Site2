from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp-pt.securemail.pro'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@solonline.pt'
app.config['MAIL_PASSWORD'] = 'M@c1000jr-'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SECRET_KEY'] = 'NSKCSDdas'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

from views import views
from auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from models import User

# Criar base de dados
if not path.exists('site/' + DB_NAME):
    db.create_all(app=app)
    print("Base de dados criada")

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message = "Por favor, faça login para acessar a esta pagina."
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    app.run(debug=True)
