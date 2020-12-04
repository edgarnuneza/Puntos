from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError
import os
from werkzeug.utils import secure_filename
from json_file import crear_json_file, leer_json_file
from sqlalchemy import ForeignKey
import json

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/imagenes_subidas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/imagen_puntos'

db = SQLAlchemy(app)
db.session.expire_on_commit = False
current_user = None
current_image = None

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

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        posible_password = request.form['password']
        
        user = Usuario.query.filter_by(user_name=user_name).first()
        
        if user:
            if user.password == posible_password:
                global current_user
                current_user = user
                return redirect(url_for("seleccionar"))
            else:
                return 'MAl'
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
        
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route("/subir_imagen", methods=['POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['archivo']
        filename = secure_filename(f.filename)

        imagen = Imagen(nombre=filename, user_name=current_user.user_name, ruta='.', ruta_puntos='.')
        
        db.session.add(imagen)
        db.session.commit()
        db.session.flush()
        
        nombre_guardar = imagen.id_imagen
        
        crear_json_file(str(nombre_guardar))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], str(nombre_guardar) + ".png"))

        imagen.ruta = '/static/imagenes_subidas/' + str(nombre_guardar) + '.png'
        imagen.ruta_puntos = 'coordenadas/' + str(nombre_guardar) + '.txt'
        db.session.commit()
        db.session.flush()
        
        global current_image 
        current_image = imagen.id_imagen
        
        return redirect(url_for('edicion'))

@app.route("/edicion", methods=['GET'])
def edicion():
    global current_user
    global current_image
    
    if not current_user:
        return redirect(url_for("login"))

    if not current_image:
        return redirect(url_for('seleccionar'))
    
    puntos = leer_json_file(str(current_image))

    return render_template("manejo_imagen.html", ubicacion_imagen='/static/imagenes_subidas/' + str(current_image) +'.png', puntos=puntos)

@app.route('/cambiar_imagen', methods=['POST'])
def cambiar_imagen():
    global current_image
        
    nombre_nueva_imagen = request.form['current_image']
    imagen = Imagen.query.filter_by(nombre=nombre_nueva_imagen).first()
    
    current_image = imagen.id_imagen
    
    return redirect(url_for("edicion"))

@app.route('/borrar_imagen', methods=['POST'])
def borrar_imagen():
    global current_image
    
    nombre_imagen_borrar = request.form['current_image']
    imagen = Imagen.query.filter_by(nombre=nombre_imagen_borrar).first()
    
    os.remove('.' + imagen.ruta)
    os.remove(imagen.ruta_puntos)
    db.session.delete(imagen)
    db.session.commit()
    db.session.flush()
    current_image = None

    return redirect(url_for('edicion'))

@app.route('/seleccionar')
def seleccionar():
    global current_user
    global current_image
    
    current_image = None
    imagenes_guardadas = Imagen.query.filter_by(user_name=current_user.user_name).order_by(Imagen.id_imagen.desc()).all()
    
    return render_template('escoger_imagen.html', imagenes=imagenes_guardadas)    

@app.route('/guardar', methods=['POST'])
def guardar():
    global current_image
    puntos = request.form['puntos']
    
    _puntos = json.loads(puntos)
    
    with open('coordenadas/'+ str(current_image) +'.txt', 'w') as outfile:
        json.dump(_puntos, outfile)
    
    return redirect(url_for('edicion'))
    
@app.route('/enviar_imagen', methods=['POST'])
def enviarimg():
    id_imagen = request.form['id']
    global current_image
    current_image = id_imagen
    return redirect(url_for('edicion'))


if __name__ == '__main__':
    app.run(debug=True) 