import re

# Mensaje original
#mensaje = "¡Gracias, Luis Gómez! Un integrante de Greengol se contactará contigo pronto para agendar la cita. (Nombre: Luis Gómez Correo electrónico: luis@gmail.com Teléfono: 3700892727 Motivo de la cita: mi vivienda tiene una estructura compleja asi que me gustaría agendar una cita para una evaluación personalizada.) Para continuar, por favor escriba: greenglocotiza."

def eraserx(mensaje):
    coincidencias = re.search(
    r"^(?P<nombre>\w+(?:\s\w+)?),?\s.*?(?P<correo>\w+@\w+\.\w+),?\s.*?(?P<telefono>\d+),?\s(?P<comentario>.+)$", 
    mensaje
    )

    if coincidencias:
        nombre = coincidencias.group("nombre")
        correo = coincidencias.group("correo")
        telefono = coincidencias.group("telefono")
        comentario = coincidencias.group("comentario")
    else:
        nombre = correo = telefono = comentario = "No encontrado"

    # Imprimir la información extraída
    print("Nombre:", nombre)
    print("Correo:", correo)
    print("Teléfono:", telefono)
    print("Comentario:", comentario)

    # Eliminar la información del mensaje original
    mensaje_limpio = re.sub(r"\w+@\w+\.\w+.*?\d+\s", "", mensaje)

    # Imprimir el mensaje limpio
    print("\nMensaje limpio:", mensaje_limpio)
    return nombre, correo, telefono, comentario
