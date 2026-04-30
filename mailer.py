from flask import render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# mailer.py[cite: 11]
import smtplib
from email.mime.text import MIMEText

# En mailer.py - Nueva versión robusta
from flask import render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_recuperacion(destinatario, nombre_usuario, token):
    config = {
        "host": "sandbox.smtp.mailtrap.io",
        "port": 587, 
        "user": "5a720ed8f5d3b2",
        "pass": "36c34c2abb0c2e" 
    }

    # 1. Preparamos el enlace y renderizamos el HTML
    enlace = f"http://localhost:5000/reset/{token}"
    html_renderizado = render_template(
        "email_recuperacion.html", 
        nombre=nombre_usuario, 
        enlace=enlace
    )

    # 2. Creamos un mensaje Multipart (necesario para enviar HTML)
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Recuperación de Acceso - Librería Virtual"
    mensaje["From"] = "soporte@libreria.com"
    mensaje["To"] = destinatario

    # 3. Adjuntamos el contenido HTML
    mensaje.attach(MIMEText(html_renderizado, "html"))

    try:
        # 4. Protocolo de envío seguro
        server = smtplib.SMTP(config["host"], config["port"], timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config["user"], config["pass"])
        server.send_message(mensaje)
        server.quit()
        print("Correo HTML enviado correctamente a Mailtrap")
        return True
    except Exception as e:
        print(f"Error al enviar HTML: {e}")
        return False

def enviar_confirmacion_compra(destinatario, nombre_usuario, datos_carrito):
    config = {
        "host": "sandbox.smtp.mailtrap.io",
        "port": 587, 
        "user": "5a720ed8f5d3b2", # Asegúrate de que no hay espacios
        "pass": "36c34c2abb0c2e" 
    }

    # Renderizamos la plantilla pasando los datos del carrito[cite: 2]
    html_renderizado = render_template(
        "email_compra.html", 
        nombre=nombre_usuario, 
        items=datos_carrito['items'], 
        total=datos_carrito['total']
    )

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Confirmación de Pedido #12345 - Librería Virtual"
    mensaje["From"] = "pedidos@libreriavirtual.com"
    mensaje["To"] = destinatario
    mensaje.attach(MIMEText(html_renderizado, "html"))

    try:
        with smtplib.SMTP(config["host"], config["port"]) as server:
            server.starttls()
            server.login(config["user"], config["pass"])
            server.send_message(mensaje)
        return True
    except Exception as e:
        print(f"Error envío compra: {e}")
        return False