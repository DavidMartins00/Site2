from io import TextIOWrapper

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user
from secrets import token_hex

from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, mail
from models import Variavel, Easc, Asc, Cliente, User

import csv

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def main():  # put application's code here
    return render_template("index.html", user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count())


@views.route('/mm')
@login_required
def manut():  # put application's code here
    return render_template("manut.html", user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count(), dados=Asc.query.all(), edados=Easc.query.all(),
                           err=db.session.query(Easc).count())


# Apagar Registro
@views.route('/mm/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def apagar(id):
    reg = Asc.query.get_or_404(id)
    if reg:
        db.session.delete(reg)
        db.session.commit()
        flash("Registro Apagado")
    else:
        pass
    return redirect(url_for('views.manut'))


@views.route('/mm/<int:id>/edelete', methods=['GET', 'POST'])
@login_required
def eapagar(id):
    reg = Easc.query.get_or_404(id)
    if reg:
        db.session.delete(reg)
        db.session.commit()
    else:
        pass
    return redirect(url_for('views.manut'))


@views.route('/mm/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    data = Asc.query.get_or_404(id)
    if request.method == 'POST':
        if data:
            nome = request.form.get('nome')
            email = request.form.get('email')
            tele = request.form.get('tele')
            pais = request.form.get('pais')
            perfil1 = request.form.get('perfil1')
            perfil2 = request.form.get('perfil2')

            if nome == "" or email == "" or tele == "" or pais == "" or perfil1 == "" or perfil2 == "":
                elin = Easc(nome=nome, email=email, tele=tele, pais=pais, perfil1=perfil1, perfil2=perfil2)
                db.session.add(elin)
                db.session.delete(data)
            else:
                data.nome = nome
                data.email = email
                data.tele = tele
                data.pais = pais
                data.perfil1 = perfil1
                data.perfil2 = perfil2
            db.session.commit()
            return redirect(url_for('views.manut'))

    return render_template('editreg.html', data=data, user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count(), err=db.session.query(Easc).count())


@views.route('/mm/<int:id>/eupdate', methods=['GET', 'POST'])
@login_required
def eupdate(id):
    data = Easc.query.get_or_404(id)

    if request.method == 'POST':
        if data:
            nome = request.form.get('nome')
            email = request.form.get('email')
            tele = request.form.get('tele')
            pais = request.form.get('pais')
            perfil1 = request.form.get('perfil1')
            perfil2 = request.form.get('perfil2')

            if nome == "" or email == "" or tele == "" or pais == "" or perfil1 == "" or perfil2 == "":
                data.nome = nome
                data.email = email
                data.tele = tele
                data.pais = pais
                data.perfil1 = perfil1
                data.perfil2 = perfil2
                db.session.commit()
            else:
                mov = Asc(nome=nome, email=email, tele=tele, pais=pais, perfil1=perfil1, perfil2=perfil2)
                db.session.add(mov)
                db.session.delete(data)
                db.session.commit()
            return redirect(url_for('views.manut'))

    return render_template('editreg.html', data=data, user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count(), err=db.session.query(Easc).count())


@views.route('/importacao', methods=['GET', 'POST'])
@login_required
def importacao():
    var = Variavel.query.get(1)
    if not var:
        var = Variavel(count=0, ecount=0)
        db.session.add(var)
        db.session.commit()
    count = 0
    ecount = 0
    if request.method == 'POST':
        # Ir buscar dados ao html
        nome = request.form.get('nome')
        email = request.form.get('email')
        tele = request.form.get('tele')
        pais = request.form.get('pais')
        perfil1 = request.form.get('perfil1')
        perfil2 = request.form.get('perfil2')
        # Adicionar na bd
        if nome == "" or email == "" or tele == "" or pais == "" or perfil1 == "" or perfil2 == "":
            ecount += 1
            elin = Easc(nome=nome, email=email, tele=tele, pais=pais, perfil1=perfil1, perfil2=perfil2)
            db.session.add(elin)
            db.session.commit()
        else:
            count += 1
            mov = Asc(nome=nome, email=email, tele=tele, pais=pais, perfil1=perfil1, perfil2=perfil2)
            db.session.add(mov)
            db.session.commit()
        var.count = count
        var.ecount = ecount
        db.session.commit()
        return redirect(url_for('views.main'))
    return render_template("importa.html", user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count())


@views.route('/uploadcsv', methods=['GET', 'POST'])
@login_required
def uploadcsv():
    var = Variavel.query.get(1)
    if request.method == 'POST':
        count = 0
        ecount = 0

        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')

        csv_reader = csv.reader(csv_file)
        for dt in csv_reader:
            row = ["", "", "", "", "", ""]
            if 0 < len(dt):
                row[0] = dt[0]
                if 1 < len(dt):
                    row[1] = dt[1]
                    if 2 < len(dt):
                        row[2] = dt[2]
                        if 3 < len(dt):
                            row[3] = dt[3]
                            if 4 < len(dt):
                                row[4] = dt[4]
                                if 5 < len(dt):
                                    row[5] = dt[5]

            if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "" or row[4] == "" or row[5] == "":
                ecount += 1
                elin = Easc(nome=row[0], email=row[1], tele=row[2], pais=row[3], perfil1=row[4], perfil2=row[5])
                db.session.add(elin)
            else:
                if not row[0] == "Nome":
                    count += 1
                    lin = Asc(nome=row[0], email=row[1], tele=row[2], pais=row[3], perfil1=row[4], perfil2=row[5])
                    db.session.add(lin)

        var.count = count
        var.ecount = ecount
        db.session.commit()
        return redirect(url_for('views.main'))


@views.route('/cliente', methods=['GET', 'POST'])
@login_required
def cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        role = request.form.get('cargo')

        tokenn = token_hex(255)
        clt = Cliente.query.filter_by(email=email).first()
        usr = User.query.filter_by(email=email).first()
        if not clt and not usr:
            msg = Message('Configuração Conta Solonline', sender='info@solonline.pt', recipients=[email])
            msg.html = """<div>
                <p>Prezado Cliente, sua conta foi criada e neste momento precisamos validar seu e-mail e
                    completar seu cadastro. Por favor clique no link abaixo para ter acesso ao seu ambiente
                    de trabalho.</p>
                <br>
                <p>Atenciosamente,
                    Equipe Sol On-line</p>
            </div>
            <div class="text-center text-muted mb-4">
                <a href="https://app.solonline.pt/criarconta/""" + tokenn + """" class="btn btn-info">Cadastro</a>
            </div>"""
            try:
                mail.send(msg)
                cliente = Cliente(nome=nome, email=email, role=role, tokenn=tokenn)
                db.session.add(cliente)
                db.session.commit()
                flash("Conta Criada")
            except:
                flash("Email não existe", category="error")
        else:
            flash("Email já em uso", category="error")
    return render_template("cliente.html", user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(User).count(), nc=db.session.query(Cliente).count(),
                           dados=User.query.all(), edados=Cliente.query.all())


@views.route('/cliente/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def dcliente(id):
    reg = Cliente.query.get_or_404(id)
    if reg:
        db.session.delete(reg)
        db.session.commit()
    else:
        pass
    return redirect(url_for('views.cliente'))


@views.route('/cliente/<int:id>/reset', methods=['GET', 'POST'])
@login_required
def rcliente(id):
    reg = Cliente.query.get_or_404(id)
    if reg:
        nome = reg.nome
        email = reg.email
        db.session.delete(reg)
        db.session.commit()
        tokenn = token_hex(255)
        msg = Message('Configuração Conta Solonline', sender='info@solonline.pt', recipients=[email])
        msg.html = """<div>
    <p>Prezado Cliente, sua conta foi criada e neste momento precisamos validar seu e-mail e
        completar seu cadastro. Por favor clique no link abaixo para ter acesso ao seu ambiente
        de trabalho.</p>
    <br>
    <p>Atenciosamente,
        Equipe Sol On-line</p>
</div>
<div class="text-center text-muted mb-4">
    <a href="https://app.solonline.pt/criarconta/""" + tokenn + """" class="btn btn-info">Cadastro</a>
</div>"""
        try:
            mail.send(msg)
            cliente = Cliente(nome=nome, email=email, tokenn=tokenn)
            db.session.add(cliente)
            db.session.commit()
            flash("Conta Criada")
        except:
            flash("Email não existe", category="error")
    else:
        pass
    return redirect(url_for('views.cliente'))


@views.route('/criarconta/<tokenn>', methods=['GET', 'POST'])
def criarconta(tokenn):
    tokn = Cliente.query.filter_by(tokenn=tokenn).first()
    if request.method == 'POST':
        password = request.form.get('pass')
        nif = request.form.get('nif')
        tel = request.form.get('tel')
        telf = request.form.get('telf')
        morada = request.form.get('morada')
        perfil1 = request.form.get('perfil1')
        perfil2 = request.form.get('perfil2')
        leads = request.form.get('leads')
        tpag = request.form.get('tpag')

        if password != "":
            usr = User(email=tokn.email, name=tokn.nome, password=generate_password_hash(password, method='sha256'),
                       role=tokn.role, nif=nif, tel=tel, telf=telf, morada=morada, perfil1=perfil1, perfil2=perfil2,
                       leads=leads, tipop=tpag)
            db.session.add(usr)
            db.session.delete(tokn)
            db.session.commit()

            user = User.query.filter_by(email=tokn.email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Conta criada com sucesso", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for('views.main'))

    if tokn:
        return render_template("criar.html", emaill=tokn.email, name=tokn.nome)
    else:
        return "Token Errado"


@views.route('/user/<int:id>/update', methods=['GET', 'POST'])
@login_required
def euser(id):
    data = User.query.get_or_404(id)

    if request.method == 'POST':
        if data:
            data.email = request.form.get('email')
            data.name = request.form.get('name')
            data.role = request.form.get('role')
            data.nif = request.form.get('nif')
            data.tel = request.form.get('tel')
            data.telf = request.form.get('telf')
            data.morada = request.form.get('morada')
            data.perfil1 = request.form.get('perfil1')
            data.perfil2 = request.form.get('perfil2')
            data.leads = request.form.get('leads')
            data.tipop = request.form.get('tpag')
            db.session.commit()
            return redirect(url_for('views.cliente'))

    return render_template('euser.html', data=data, user=current_user, var=Variavel.query.get(1),
                           tt=db.session.query(Asc).count(), err=db.session.query(Easc).count())


@views.route('/user/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def duser(id):
    reg = User.query.get_or_404(id)
    if reg:
        db.session.delete(reg)
        db.session.commit()
    else:
        pass
    return redirect(url_for('views.cliente'))

