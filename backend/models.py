from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    cedula = db.Column(db.String(20), nullable=True)
    fecha = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)  # antes era 'correo'
    contacto_emergencia = db.Column(db.String(100), nullable=False)
    enfermedad = db.Column(db.String(50), nullable=False)  # antes era 'enfermedad_cronica'
    alergia = db.Column(db.String(50), nullable=False)
    medicamento = db.Column(db.String(50), nullable=False)
    comentarios = db.Column(db.String, nullable=False)
    tipo_de_sangre = db.Column(db.String(20), nullable=True)

