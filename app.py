from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import Usuario, Imagen
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/imagen_puntos'

db = SQLAlchemy(app)

@app.route('/')
def index():
    #Create
    imagen = Imagen(nombre='img1', user_name='juanpz', ruta='fasd', ruta_puntos='bsdfv')
    #usuario = Usuario(user_name=5, nombre='hevtot', apellido='Hernandez', contrasena='123', ultimo_acceso=5)
    db.session.add(imagen)
    db.session.commit()

    #Read
    #usuarios_leidos = Usuario.query.all()

    #Update
    #user = Usuario.query.filter_by(user_name=5).first()
    #user.nombre = 'fiesta'
    #db.session.commit()

    #Delete
    #user_name = 5
    #user = Usuario.query.filter_by(user_name=user_name).first()
    #db.session.delete(user)
    #db.session.commit()
    return 'Que rollo'

    #return render_template("inicio.html", usuarios=usuarios_leidos)
    #return render_template("inicio.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        posible_password = request.form['password']
        
        user = Usuario.query.filter_by(user_name=user_name).first()
        
        if user is not None:
            if user.password == posible_password:
                return 'Login correcto'
            else:
                return 'Contraseña incorrecta'
        else:
            return 'Contraseña incorrecta'
    else:
        return render_template("login.html")

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        user_name = request.form['username']
        nombre = request.form['name']
        password = request.form['password']
        
        usuario = Usuario(user_name=user_name, nombre=nombre, password=password)
        
        try:
            db.session.add(usuario)
            db.session.commit()
        except IntegrityError:
            return 'Este nombre de usuario ya existe'
        
        return "jalo"
    else:
        return render_template('register.html')

#Si se ejecuta este archivo directamente, corre la apliacion. 
if __name__ == '__main__':
    app.run(debug=True) 