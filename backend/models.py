from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contacto(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), nullable=False, unique=True)
    fecha = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contacto_emergencia = db.Column(db.String(100))
    enfermedad = db.Column(db.String(200))
    alergia = db.Column(db.String(200))
    medicamento = db.Column(db.String(200))
    comentarios = db.Column(db.String(500))
    tipo_de_sangre = db.Column(db.String(3))
    codigo_qr = db.Column(db.Text, nullable=True) 


