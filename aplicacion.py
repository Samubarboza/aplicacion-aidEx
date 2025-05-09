'''#Esta funcion se encarga de crear una nuevo registro(persona)
def crear_registro():
    usuario_existente = Personas.query.filter(
        (Personas.cedula == request.form["cedula"]) |
        (Personas.correo == request.form["email"]) 
        ).first()
    
    if usuario_existente:
        return "Ya existe un usuario registrado con ese dato", 400
    
    cedula = request.form["cedula"]
    texto_qr = url_for("mostrar_persona", cedula = cedula, _external = True)
#     texto_qr = (
#     nombre = request.form['nombre']
#     fecha_nacimiento = request.form['fecha']
#     cedula = request.form['cedula']
#     correo = request.form['email']
#     tipo_de_sangre = request.form['tipoSangre']
#     alergia = request.form['alergia']
#     enfermedades crónicas = request.form['enfermedad']
#     medicamentos actuales = request.form['medicamento']
#     comentarios = request.form['comentarios']
#     contacto_emergencia = request.form['contacto']
# )

    

    imagen_qr = qrcode.make(texto_qr)
    buffer = io.BytesIO()
    imagen_qr.save(buffer, format="PNG")
    buffer.seek(0)
    imagen_base64 =  base64.b64encode(buffer.read()).decode("utf-8")
    codigo_qr = f"data:image/png;base64,{imagen_base64}"

    nuevo_registro_persona = Personas(
    nombre = request.form["nombre"],
    cedula = cedula,
    fecha = request.form["fecha"],
    correo = request.form["email"],
    contacto_emergencia = request.form["contacto"],
    enfermedad_cronica = request.form["enfermedad"],
    alergia = request.form["alergia"],
    medicamento = request.form["medicamento"],
    comentarios = request.form["comentarios"],
    tipo_de_sangre = request.form["tipoSangre"],
    codigo_qr = codigo_qr
)

    db.session.add(nuevo_registro_persona)
    db.session.commit()
    return render_template("confirmacion.html" , persona = nuevo_registro_persona)'''