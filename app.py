from flask import Flask, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib import sqla
from flask_simplelogin import SimpleLogin, login_required
from dynaconf import FlaskDynaconf
import os
# from app import app


app = Flask(__name__)

# Define o diretório base do aplicativo Flask
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define a URI do banco de dados SQLite
# sqlite_uri = 'sqlite:///' + os.path.join(base_dir, 'mydatabase.db')

# Configura a URI do banco de dados no aplicativo Flask
# app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri

# Evita avisos deprecados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
FlaskDynaconf(app)

# Inicializa a extensão SQLAlchemy passando a aplicação Flask
db = SQLAlchemy(app)

# Restante do código...
Bootstrap(app)


def verify_login(user):
    return user.get("username") == "admin" and user.get("password") == "1234"

SimpleLogin(app, login_checker=verify_login)


# proteger o admin com login via monkey patch
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
Admin(app, name=app.config.TITLE, template_mode="bootstrap3")


class Product(db.Model):
    __tablename__ = "Produto"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)

@app.cli.command()
def createdb():
    """Creates sqlite database"""
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)
 

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        abort(404, "Produto não encontrado")
    return render_template("index.html", product=product)


if __name__ == '__main__':
    with app.app_context():
        # Criar tabelas no banco de dados
        db.create_all()
    app.run(debug=True)