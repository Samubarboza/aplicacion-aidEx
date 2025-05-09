from flask import Flask, render_template, request, redirect, url_for
from backend.models import db, Contacto
from datetime import datetime
import qrcode
import io
import base64
import os

app = Flask(__name__)

# ACA TENEMOS LA CONFIGURACION DE LA BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


QR_FOLDER = 'static/qrcodes'
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('inicio.html')


@app.route('/cargar-formulario', methods=['POST'])
def datos_del_formulario():
    if request.method == 'POST':
        datos = request.form
        
    
        fecha_convertida = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()

    
        cedula_existente = Contacto.query.filter_by(cedula=datos['cedula']).first()
        email_existente = Contacto.query.filter_by(email=datos['email']).first()

        if cedula_existente or email_existente:
            return render_template('index.html', mensaje="Usuario ya registrado.")

    
        contacto = Contacto(
            nombre=datos['nombre'],
            cedula=datos['cedula'],
            fecha=fecha_convertida,
            email=datos['email'],
            contacto_emergencia=datos['contacto_emergencia'],
            enfermedad=datos['enfermedad'],
            alergia=datos['alergia'],
            medicamento=datos['medicamento'],
            comentarios=datos['comentarios'],
            tipo_de_sangre=datos['tipoSangre'],
            codigo_qr=None  
        )

        db.session.add(contacto)
        db.session.commit()

    
        texto_qr = url_for("confirmacion", id=contacto.id, _external=True)
        print(texto_qr)


        imagen_qr = qrcode.make(texto_qr)


        buffer = io.BytesIO()
        imagen_qr.save(buffer, format="PNG")
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    
        codigo_qr = f"data:image/png;base64,{imagen_base64}"

    
        contacto.codigo_qr = codigo_qr
        db.session.commit()

        return redirect(url_for('confirmacion', id=contacto.id))


@app.route('/confirmacion/<int:id>', methods=['GET'])
def confirmacion(id):
    contacto = Contacto.query.get(id)
    if not contacto:
        return render_template('registrado.html', mensaje_='Contacto no encontrado.')

    return render_template('confirmacion.html', contacto=contacto)

# Rutas 
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/consultar')
def consultar():
    return render_template('registrado.html')

@app.route('/sobrenosotros')
def sobre_nosotros():
    return render_template('sobrenosotros.html')

@app.route('/tyc')
def terminos_y_condiciones():
    return render_template('tyc.html')

@app.route('/buscar', methods=['POST'])
def buscar_contacto():
    cedula = request.form.get('nombre')
    contacto = Contacto.query.filter_by(cedula=cedula).first()

    if contacto:
        return render_template('datos.html', contacto=contacto)
    else:
        return render_template('registrado.html', mensaje_='¡No se encontró contacto con esa cédula!')


if __name__ == '__main__':
    app.run(debug=True)
