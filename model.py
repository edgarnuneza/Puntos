from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/imagen_puntos'

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    user_name = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(15), nullable=False)

class Imagen(db.Model): 
    __tablename__ = 'imagen'
    id_imagen = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), ForeignKey('usuario.user_name'), nullable = False)
    ruta = db.Column(db.String(200), nullable=False)
    ruta_puntos = db.Column(db.String(200), nullable=False)