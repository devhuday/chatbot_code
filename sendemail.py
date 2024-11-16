import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Credenciales de Gmail
EMAIL_USER = "botgreenglo@gmail.com"
EMAIL_PASSWORD = "iamo tirh hudn naav"

def enviar_correo(destinatario, asunto, mensaje, footer):
    # Configuración del servidor SMTP de Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_PASSWORD)

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = asunto
    #msg.attach(MIMEText(mensaje, 'html'))

    # Cargar la plantilla HTML
    with open("plantilla.html", "r", encoding="utf-8") as archivo:
        plantilla_html = archivo.read()
    plantilla_html = plantilla_html.replace("{nombre}", asunto)
    plantilla_html = plantilla_html.replace("{textbody}", mensaje)
    plantilla_html = plantilla_html.replace("{footer}", footer)
    # Adjuntar la plantilla HTML al correo
    msg.attach(MIMEText(plantilla_html, 'html'))

    # Enviar el correo
    servidor.sendmail(EMAIL_USER, destinatario, msg.as_string())
    servidor.quit()

    print("Correo enviado exitosamente a", destinatario)


def loadcorreo(nombre, correo, telefono, comentario):
    # Ejemplo de uso
    #destinatario = "ventasbot@greenglo.com.co"
    destinatario = "hudaayy14@gmail.com"
    asunto = "Petición reunion Greenglo"
    footer = "<b>Equipo Greenglo S.A.S.</b> "

    encargado = "Heiner"

    mensaje = f""" <br><br>¡Hola {encargado}!<br>

    Tienes una nueva solicitud de cita de {nombre}.<br>

    Aquí tienes la información del cliente:<br><br>

    <b>Nombre:</b> {nombre}<br>
    <b>Correo electrónico:</b> {correo} <br>
    <b>Teléfono:</b> {telefono}<br>
    <b>Motivo de la cita:</b> {comentario}<br><br>
    Por favor, contacta con {nombre} lo antes posible para confirmar<br>
    la cita y coordinar los detalles.<br>

    ¡Esperamos que tengas una excelente reunión!<br>

    Atentamente...<br><br>
    """
    return destinatario, asunto, mensaje, footer
