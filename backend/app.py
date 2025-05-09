from flask import Flask, render_template, request, redirect, url_for
from backend.models import db, Contacto
from datetime import datetime
import qrcode
import io
import base64
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Carpeta para guardar los códigos QR
QR_FOLDER = 'static/qrcodes'
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('inicio.html')

# Ruta para procesar el formulario
@app.route('/cargar-formulario', methods=['POST'])
def datos_del_formulario():
    if request.method == 'POST':
        datos = request.form
        
        # Convertir la fecha
        fecha_convertida = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()

        # Verificar si ya existe el contacto
        cedula_existente = Contacto.query.filter_by(cedula=datos['cedula']).first()
        email_existente = Contacto.query.filter_by(email=datos['email']).first()

        if cedula_existente or email_existente:
            return render_template('index.html', mensaje="Usuario ya registrado.")

        # Crear el contacto sin QR
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
            codigo_qr=None  # Se actualizará después con base64
        )

        db.session.add(contacto)
        db.session.commit()  # Se guarda para obtener el ID

        # Crear el texto para el QR
        texto_qr = url_for("confirmacion", id=contacto.id, _external=True)
        print(texto_qr)

        # Generar la imagen QR
        imagen_qr = qrcode.make(texto_qr)

        # Convertir la imagen QR a base64
        buffer = io.BytesIO()
        imagen_qr.save(buffer, format="PNG")
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        # Crear el código QR en base64
        codigo_qr = f"data:image/png;base64,{imagen_base64}"

        # Actualizar el contacto con el código QR
        contacto.codigo_qr = codigo_qr
        db.session.commit()

        # Redirigir a la página de confirmación
        return redirect(url_for('confirmacion', id=contacto.id))

# Ruta para mostrar la confirmación con el QR
@app.route('/confirmacion/<int:id>', methods=['GET'])
def confirmacion(id):
    contacto = Contacto.query.get(id)
    if not contacto:
        return render_template('registrado.html', mensaje_='Contacto no encontrado.')

    return render_template('confirmacion.html', contacto=contacto)

# Rutas adicionales
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

# Correr la app
if __name__ == '__main__':
    app.run(debug=True)
