import re

# Mensaje original
#mensaje = "¡Gracias, Luis Gómez! Un integrante de Greengol se contactará contigo pronto para agendar la cita. (Nombre: Luis Gómez Correo electrónico: luis@gmail.com Teléfono: 3700892727 Motivo de la cita: mi vivienda tiene una estructura compleja asi que me gustaría agendar una cita para una evaluación personalizada.) Para continuar, por favor escriba: greenglocotiza."

def eraser(mensaje):
    # Extraer datos usando expresiones regulares
    nombre = re.search(r'Nombre: (.+?) Correo electrónico', mensaje).group(1).strip()
    correo = re.search(r'Correo electrónico: (.+?) Teléfono', mensaje).group(1).strip()
    telefono = re.search(r'Teléfono: (.+?) Motivo de la cita', mensaje).group(1).strip()
    comentario = re.search(r'Motivo de la cita: (.+?)\)', mensaje).group(1).strip()

    # Quitar los datos del mensaje original
    mensaje_modificado = re.sub(r'\(Nombre: .+? Motivo de la cita: .+?\)', '', mensaje).strip()

    # Resultados
    print("Nombre:", nombre)
    print("Correo:", correo)
    print("Teléfono:", telefono)
    print("Comentario:", comentario)
    print("Mensaje modificado:", mensaje_modificado)
    return nombre, correo, telefono, comentario, mensaje_modificado
