from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import Usuario, Imagen
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename
from json_file import crear_json_file, leer_json_file

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/imagenes_subidas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/imagen_puntos'

db = SQLAlchemy(app)
current_user = None
current_image = None

@app.route('/')
def index():
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        posible_password = request.form['password']
        
        user = Usuario.query.filter_by(user_name=user_name).first()
        
        if user is not None:
            if user.password == posible_password:
                global current_user
                current_user = user
                return redirect(url_for("edicion"))
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
        
        return "jalo"
    else:
        return render_template('register.html')

@app.route('/subir')
def subir():
    return render_template("subir_imagen.html")


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

        return "<h1>Archivo subido exitosamente</h1>"

@app.route("/edicion", methods=['POST', 'GET'])
def edicion():
    if not current_user:
        return redirect(url_for("login"))
    
    imagenes_guardadas = Imagen.query.filter_by(user_name=current_user.user_name).order_by(Imagen.id_imagen.desc()).all()

    nombre_imagenes = []
    
    for imagen in imagenes_guardadas:
        nombre_imagenes.append(imagen.nombre)
    
    global current_image
    
    if not current_image:
        current_image = imagenes_guardadas[0]
        print(current_image.id_imagen)
    
    puntos = leer_json_file(str(current_image.id_imagen))
    
    return render_template("manejo_imagen.html", ubicacion_imagen='/static/imagenes_subidas/' + str(current_image.id_imagen) +'.png', nombre_imagenes=nombre_imagenes, puntos=puntos)

@app.route('/imagen')
def imagen():
    return render_template("imagen.html")

@app.route('/cambiar_imagen', methods=['POST'])
def cambiar_imagen():
    if request.method == 'POST':
        global current_image
        nombre_nueva_imagen = request.form['current_image']
        imagen = Imagen.query.filter_by(nombre=nombre_nueva_imagen).first()

        current_image = imagen

        return redirect(url_for("edicion"))

if __name__ == '__main__':
    app.run(debug=True) 