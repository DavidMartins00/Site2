# Admin>Gerente>Supervisor>Operador
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

ACCESS = {
    'Cliente': 0,
    'Parceiro': 1,
    'Parceiro25': 1,
    'Parceiro50': 1,
    'Parceiro100': 1,
    'Colaborador': 2,
    'Supervisor': 3,
    'Admin': 99
}


def roles(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not ACCESS[current_user.role] >= ACCESS[role]:
                # Redirect the user to an unauthorized notice!
                flash("Não tem permissão para aceder a esta pagina!", category="error")
                return redirect(url_for('views.main'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper
