import flask_login
from flask import render_template, Blueprint
from flask_login import current_user, login_required

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def main():  # put application's code here
    return render_template("index.html", user=current_user)
