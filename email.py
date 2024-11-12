import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Credenciales de Gmail
EMAIL_USER = "botgreenglo@gmail.com"
EMAIL_PASSWORD = "iamo tirh hudn naav"

def enviar_correo(destinatario, asunto, mensaje):
    # Configuración del servidor SMTP de Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_PASSWORD)

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Enviar el correo
    servidor.sendmail(EMAIL_USER, destinatario, msg.as_string())
    servidor.quit()

    print("Correo enviado exitosamente a", destinatario)

