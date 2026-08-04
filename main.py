"""app"""

from flask import Flask, render_template, request
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "conectiacol@gmail.com"
app.config["MAIL_PASSWORD"] = "vhrsstieciiqkzqr"
app.config["MAIL_DEFAULT_SENDER"] = "conectiacol@gmail.com"

mail = Mail(app)


def conectar_db():
    return sqlite3.connect("citas.db")


@app.route("/")
def inicio():
    return render_template("index.html")


def verificar_cita(fecha, hora):

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT fecha, hora FROM citas
    """)

    citas = cursor.fetchall()
    conexion.close()

    for cita in citas:

        if fecha == cita[0] and hora == cita[1]:
            return True

    return False

def obtener_citas():

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM citas")

    citas = cursor.fetchall()

    conexion.close()

    return citas

@app.route("/admin")
def admin():
    citas = obtener_citas()

    return render_template(
        "admin.html",
        citas=citas
    )


@app.route("/agendar", methods=["POST"])
def agendar():

    nombre = request.form["nombre"]
    telefono = request.form["telefono"]
    gmail = request.form["gmail"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    historia = request.form.get("historia")


    if verificar_cita(fecha, hora):
        return render_template(
        "error.html",
        fecha=fecha,
        hora=hora
    )


    conexion = conectar_db()

    conexion.execute("""
    INSERT INTO citas
    (nombre, telefono, gmail, fecha, hora, historia)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (nombre, telefono, gmail, fecha, hora, historia))


    conexion.commit()
    conexion.close()


    mensaje = Message(
        "Confirmación de cita - Optikale",
        sender=app.config["MAIL_USERNAME"],
        recipients=[gmail]
    )


    mensaje.body = f"""
Hola {nombre} 👓

Tu solicitud de cita fue recibida.

Fecha: {fecha}
Hora: {hora}

Gracias por elegir Optikale.
"""


    mail.send(mensaje)

    print("Correo enviado a:", gmail)


    return render_template(
        "confirmacion.html",
        nombre=nombre,
        gmail=gmail
    )
@app.route("/completar_cita/<id>", methods=["POST"])
def eliminar_cita(id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM citas WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    return render_template(
        "admin.html")

if __name__ == "__main__":
    app.run(debug=True)
