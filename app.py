from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os 
from flask_sqlalchemy import SQLAlchemy
from models import db, Calificacion
from scrapping import scrape_all_pages

app = Flask(__name__)

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'calificaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configuración de correo (usa variables de entorno en producción)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 2525))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'b1bffb437158ff')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '5a67c1bc142238')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mail', methods=['POST', 'GET'])
def send_email():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(
            'Hola Gustavo , tienes un nuevo contacto desde la web:',
            body=f'Nombre: {name}\nCorreo: <{email}>\n Escribió: \n\n{message}',
            sender=email,
            recipients=['vazquezmicky@gmail.com']
        )
        mail.send(msg)
        return render_template('send_mail.html')
    
    return redirect(url_for('index'))

# @app.route('/actualizar_calificaciones')
# def actualizar_calificaciones():
#     datos_scraping = scrape_calificaciones()
#     for dato in datos_scraping:
#         calificacion = Calificacion(
#             clase=dato['class'],
#             calificacion=dato['score'],
#             fecha=dato['date'],
#             comentario=dato['comment']
#         )
#         db.session.add(calificacion)
#     db.session.commit()
#     return "Calificaciones actualizadas"

@app.route('/calificaciones')
def calificaciones():
    try:
        data = scrape_all_pages()  
        return render_template('calificaciones.html', results=data)
    except Exception as e:
        print(f"Error al obtener calificaciones: {e}")
        return render_template('calificaciones.html', results=[], error="No se pudieron obtener las calificaciones")
if __name__ == '__main__':
    app.run(debug=True)