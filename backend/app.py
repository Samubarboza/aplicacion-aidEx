from flask import Flask, render_template, request, redirect
from backend.models import db, Contacto
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/cargar-formulario', methods=['POST'])
def datos_del_formulario():
    if request.method == 'POST':
        datos = request.form
        
        fecha_convertida = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
        

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
            tipo_de_sangre=datos['tipoSangre']
        )
        
        cedula_existente = Contacto.query.filter_by(cedula=datos['cedula']).first()
        email_existente = Contacto.query.filter_by(email=datos['email']).first()

        if cedula_existente or email_existente:
            return render_template('index.html', mensaje="Usuario ya registrado.")

        
        
        db.session.add(contacto)
        db.session.commit()
        

        mensaje = "¡Registro completado con éxito!"
        

        return render_template('index.html', mensaje=mensaje)

# Rutas
@app.route('/')
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
        # Si no se encuentra, redireccionamos o mostramos error
        return render_template('registrado.html', mensaje_=mensaje_)
mensaje_ = '¡No se encontro contacto con esa cédula!'



if __name__ == '__main__':
    app.run(debug=True)
