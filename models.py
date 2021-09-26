from datetime import datetime

from sqlalchemy import DateTime, func

from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    nif = db.Column(db.Integer(), nullable=True)
    tel = db.Column(db.Integer(), nullable=True)
    telf = db.Column(db.Integer(), nullable=True)
    tempo = db.Column(db.Integer(), default=0)
    tipo = db.Column(db.Integer(), default=0)
    campuser = db.relationship('CampUser')
    pais = db.Column(db.String(150), nullable=True)
    morada = db.Column(db.String(150), nullable=True)
    perfil1 = db.Column(db.String(150), nullable=True)
    perfil2 = db.Column(db.String(150), nullable=True)
    leads = db.Column(db.String(150), nullable=True)
    tipop = db.Column(db.String(150), nullable=True)
    #created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    nome = db.Column(db.String(150))
    valor = db.Column(db.Float)
    descr = db.Column(db.String(250))
    foto = db.Column(db.String, nullable=True)
    campanha = db.relationship('Campanha')


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    tipo = db.Column(db.String(150))
    produto = db.relationship('Produto')
    campanha = db.relationship('Campanha')


class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    campanha = db.Column(db.String(150))
    valorcamp = db.Column(db.Float)
    descr = db.Column(db.String(250))
    condicoes = db.Column(db.String(250))
    ofertas = db.Column(db.String(250))
    fotos = db.Column(db.String(250))
    campuser = db.relationship('CampUser', cascade="all, delete-orphan")
    deleted = db.Column(db.Boolean(), default=False)


class CampUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    campanha = db.Column(db.Integer, db.ForeignKey('campanha.id'))


class Asc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    tele = db.Column(db.Integer)
    pais = db.Column(db.String(150))
    perfil1 = db.Column(db.String(150), nullable=True)
    perfil2 = db.Column(db.String(150), nullable=True)


class Easc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    tele = db.Column(db.Integer, nullable=True)
    pais = db.Column(db.String(150), nullable=True)
    perfil1 = db.Column(db.String(150), nullable=True)
    perfil2 = db.Column(db.String(150), nullable=True)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Variavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    ecount = db.Column(db.Integer)


class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.DATETIME)
    qtd = db.Column(db.Integer, default=0)
    qtm = db.Column(db.Integer, default=0)
    desc = db.Column(db.Boolean, default=False)


class PaisUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    pais = db.Column(db.Integer, db.ForeignKey('pais.id'))


class Pais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paisuser = db.relationship('PaisUser')
    nome = db.Column(db.String(150))


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nome = db.Column(db.String(150))
    tokenn = db.Column(db.String(150))
    role = db.Column(db.String(150))
