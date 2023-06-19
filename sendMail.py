import smtplib

from flask import render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send_mail_fact(to, subject, html_content, image_path=None):
    # configuracion del correo
    sender_email = 'c_cloud2023@outlook.com'
    receiver_email = to
    password = 'C-cloud2023'

    # crear un mensaje multiparte y establece el encabezado
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # agrega el contenido html al objeto MIME
    msg.attach(MIMEText(html_content, 'html'))

    # agrega la imagen si es proporcionada
    if image_path:
        with open(image_path, 'rb') as file:
            # lee la imagen
            image_data = file.read()
        image = MIMEImage(image_data)
        image.add_header('Content-Disposition', 'attachment', filename='logo-lg.png')
        msg.attach(image)

    # conecta el servidor SMTP (Outlook)
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = sender_email

    # encriptacion TLS
    smtp_server = smtplib.SMTP(smtp_server, smtp_port)
    smtp_server.starttls()

    # inicia la sesion de la cuenta
    smtp_server.login(smtp_username, password)

    # envia el correo
    smtp_server.sendmail(sender_email, receiver_email, msg.as_bytes())

    # cierra la conexion con el servidor
    smtp_server.quit()


def send_mail(to, subject, message):

    # configuracion del correo
    sender_email = 'c_cloud2023@outlook.com'
    receiver_email = to
    password = 'C-cloud2023'

    # crea un mensaje multiparte y establece el encabezado
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # agrega el mensaje al objeto MIME
    msg.attach(MIMEText(message, 'plain'))

    # conecta el servidor SMTP (Outlook)
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = sender_email

    # encriptacion TLS
    smtp_server = smtplib.SMTP(smtp_server, smtp_port)
    smtp_server.starttls()

    # inicia la sesion de la cuenta
    smtp_server.login(smtp_username, password)

    # envia el correo
    smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

    # cierra la conexion con el servidor
    smtp_server.quit()

def account_deactivated_user_mail(email, name):
    # Crear un objeto de mensaje para el correo electrónico
    msg = render_template('account_deactivated.html', name=name)

    # Enviar el correo electrónico
    image_path = 'c-cloud/static/public/img/icon.png'
    send_mail_fact(email, 'Su cuenta ha sido desactivada', msg, image_path=image_path)

def account_deactivated_admin_mail(email, name):
    # Crear un objeto de mensaje para el correo electrónico
    msg = render_template('account_deactivated_admin.html', name=name)

    # Enviar el correo electrónico
    image_path = 'c-cloud/static/public/img/icon.png'
    send_mail_fact(email, 'Su cuenta ha sido desactivada', msg, image_path=image_path)

def password_changed_mail(email, name):
    # Crear un objeto de mensaje para el correo electrónico
    msg = render_template('password_changed.html', name=name)

    # Enviar el correo electrónico
    image_path = 'c-cloud/static/public/img/icon.png'
    send_mail_fact(email, 'Su cuenta ha sido desactivada', msg, image_path=image_path)