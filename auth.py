from flask import Blueprint, render_template, request, flash, url_for, redirect
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('pass')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, senha):
                flash("Loggedin com sucesso", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.main'))
            else:
                flash("Credenciais erradas", category="error")
    return render_template("login.html", user=current_user)


# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Registrar Utilizador
@auth.route('/register', methods=['GET', 'POST'])
# @roles("Admin")
def register():
    if request.method == 'POST':
        # Ir buscar dados ao html
        email = request.form.get('email')
        nome = request.form.get('name')
        password = request.form.get('pass')

        # Validações

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email ja existe", category="error")
        elif len(email) < 4:
            flash("Email requerido", category="error")
        elif len(nome) < 2:
            flash("Nome requerido", category="error")

        elif len(password) < 7:
            flash("Password precisa ser maior que 7 caracters", category="error")

        else:
            # Adicionar user na bd
            new_user = User(email=email, name=nome, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Conta criada", category="success")
            return redirect(url_for('views.main'))

    return render_template("register.html", user=current_user)
