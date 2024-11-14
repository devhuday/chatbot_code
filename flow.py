from services import *
import textbot as bot
import sett
import database
import ia
import sendemail
import history
import eraser

# Diccionario de respuestas
responses = {
    "hola": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
    "cotizacion": {"body": bot.nameandnumber["message"]},
    "agendar cita": {"body": bot.agendar["message"]},
    "cotizar": {"question": bot.cotizacion["message"], "options": bot.cotizacion["option"], "list": "on"},
    "on grid": {"question": bot.cotizacion_grid["message"], "options": bot.cotizacion_grid["option"]},
    "off grid": {"question": bot.cotizacion_offgrid["message"], "options": bot.cotizacion_offgrid["option"]},
    "residencial": {"question": bot.Residencial["message"], "options": bot.Residencial["option"]},
    "me parece costoso": {"body": bot.Residencial_coti_costoso["message"]},
    "si, deseo cotizar": {"body": bot.Residencial_cotizar["message"], "question": bot.Residencial_cotizar["question"], "options": bot.Residencial_cotizar["option"], "media": ("consumo", "image")},
    "menor a 1000kwh": {"question": bot.Residencial_coti_menor["message"], "options": bot.Residencial_coti_menor["option"]},
    "entre 1000 y 2000kwh": {"question": bot.Residencial_coti_entre["message"], "options": bot.Residencial_coti_entre["option"]},
    "mayor a 2000kwh": {"body": bot.Residencial_coti_mayor["message"], "contact": ("name", "number")},
    "industrial": {"body": bot.Residencial_coti_mayor["message"], "contact": ("name", "number")},
    "ahorro hasta": {"body": bot.Residencial_coti_pdf["message"], "media": ("cotizacion_", "documents")},
    "no, gracias.": {"body": "Perfecto! No dudes en contactarnos si tienes más preguntas. ¡Hasta luego! 😊"}
}

response_IA = {
    "no estoy seguro": {"responseIA": "no estoy seguro sobre qué tipo de sistema solar utilizar on grid o off grid"},
    "Desconozco estos temas": {"responseIA": "Desconozco estos temas de tipos sistema solar on grid, off grid e hibrido"}
}

footer = "Equipo Greenglo"

# Función para enviar diferentes tipos de mensajes
def enviar_mensaje(number, data, conver, message_id=None):
    responses = []
    
    # Media (imágenes o documentos)
    if "media" in data:
        media_id, media_type = data["media"]
        if media_type == "image":
            response = image_Message(number, get_media_id(media_id, media_type), data.get("body", ""))
        elif media_type == "documents":
            media_id = media_id + number[13:-3] if "cotizacion_" in media_id else media_id
            response = document_Message(
                number,
                sett.documents[f"cotizacion_{number[13:-3]}"],
                data.get("body", ""),
                f"Cotización {number[13:-3]} kwh.pdf"
            )
        responses.append(response)
        conver.new_message("bot_Greengol", data.get("body", ""))
    
    # Texto
    if "body" in data and "media" not in data:
        response = text_Message(number, data["body"])
        responses.append(response)
        conver.new_message("bot_Greengol", data["body"])
    
    # Botones
    if "options" in data:
        response = (
            listReply_Message(number, data["options"], data["question"], footer, "sed1", message_id)
            if data.get("list") == "on"
            else buttonReply_Message(number, data["options"], data["question"], footer, "sed1", message_id)
        )
        responses.append(response)
        conver.new_message("bot_Greengol", data["question"])
    
    # Contactos
    if "contact" in data:
        name_id, number_id = data["contact"]
        response = contact_Message(number, sett.contact[name_id], sett.contact[number_id])
        responses.append(response)
    
    # Respuestas de IA
    if "responseIA" in data:
        prompt = data["responseIA"]
        ia_response = ia.Request(prompt)
        response = text_Message(number, ia_response)
        responses.append(response)
    
    return responses

# Procesar respuesta
def procesar_respuesta(response_dict, text, number, message_id, conver):
    for keyword, data in response_dict.items():
        if keyword in text:
            return enviar_mensaje(number, data, conver, message_id)
    return None

# Manejar la lógica de respuestas IA
def manejar_IA(text, number, message_id, name, conver):
    responses = procesar_respuesta(response_IA, text, number, message_id, conver)
    if responses:
        for response in responses:
            enviar_Mensaje_whatsapp(response)
    else:
        ia_response = ia.Request(text)
        enviar_Mensaje_whatsapp(text_Message(number, ia_response))
        conver.new_message("bot_Greengol", ia_response)

# Función principal para manejar el chatbot
def administrar_chatbot(text, number, message_id, name):
    text = text.lower()
    conver = database.Conversacion(number, message_id, name)
    
    if not conver.check_User():
        conver.new_user()
    conver.new_message("usuario", text)
    
    enviar_Mensaje_whatsapp(markRead_Message(message_id))
    
    responses = procesar_respuesta(responses, text, number, message_id, conver)
    if responses:
        for response in responses:
            enviar_Mensaje_whatsapp(response)
    else:
        manejar_IA(text, number, message_id, name)
