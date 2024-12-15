import re

# Mensaje original
#mensaje = "¡Gracias, Luis Gómez! Un integrante de Greengol se contactará contigo pronto para agendar la cita. (Nombre: Luis Gómez Correo electrónico: luis@gmail.com Teléfono: 3700892727 Motivo de la cita: mi vivienda tiene una estructura compleja asi que me gustaría agendar una cita para una evaluación personalizada.) Para continuar, por favor escriba: greenglocotiza."

def eraserx(mensaje):
    
    
    nombre_match = re.search(r"^\w+\s\w+", mensaje)
    nombre = nombre_match.group(0) if nombre_match else "No encontrado"

    # 2. Buscar el correo electrónico
    correo_match = re.search(r"\w+@\w+\.\w+", mensaje)
    correo = correo_match.group(0) if correo_match else "No encontrado"

    # 3. Buscar el número de teléfono (7 a 10 dígitos)
    telefono_match = re.search(r"\d{8,11}", mensaje)
    telefono = telefono_match.group(0) if telefono_match else "No encontrado"

    # 4. Capturar el comentario (todo después del último dato conocido)
    comentario_match = re.search(r"\d{7,10}[,.]?\s*(.+)$", mensaje)
    comentario = comentario_match.group(1) if comentario_match else "No encontrado"
    comentario = "No encontrado" if correo in comentario else comentario
    # Imprimir resultados
    print("Nombre:", nombre)
    print("Correo:", correo)
    print("Teléfono:", telefono)
    print("Comentario:", comentario)

    # Mensaje limpio (opcional, elimina datos extraídos)
    mensaje_limpio = re.sub(r"(\w+@\w+\.\w+|\d{7,10}|^\w+\s\w+[,.\s]*)", "", mensaje).strip()
    print("\nMensaje limpio:", mensaje_limpio)

    return nombre, correo, telefono, comentario
