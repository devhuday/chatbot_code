import re

# Mensaje original
#mensaje = "¡Gracias, Luis Gómez! Un integrante de Greengol se contactará contigo pronto para agendar la cita. (Nombre: Luis Gómez Correo electrónico: luis@gmail.com Teléfono: 3700892727 Motivo de la cita: mi vivienda tiene una estructura compleja asi que me gustaría agendar una cita para una evaluación personalizada.) Para continuar, por favor escriba: greenglocotiza."

def eraserx(mensaje):
  # Extraer la información
  nombre = re.search(r"Nombre: (.+?)\s", mensaje).group(1)
  correo = re.search(r"Correo electrónico: (.+?)\s", mensaje).group(1)
  telefono = re.search(r"Teléfono: (.+?)\s", mensaje).group(1)
  comentario = re.search(r"Motivo de la cita: (.+?)\s", mensaje).group(1)

  # Imprimir la información extraída
  print("Nombre:", nombre)
  print("Correo:", correo)
  print("Teléfono:", telefono)
  print("Comentario:", comentario)

  # Eliminar la información del mensaje original
  mensaje_limpio = re.sub(r"Nombre: .+? Teléfono: .+? Motivo de la cita: .+?\s", "", mensaje)

  # Imprimir el mensaje limpio
  print("\nMensaje limpio:", mensaje_limpio)

  return nombre, correo, telefono, comentario, mensaje_limpio

