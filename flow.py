
from services import *
import textbot as bot
import sett
import database
import ia
import sendemail 
import history
import eraser
from unidecode import unidecode

# Diccionario para almacenar los mensajes
RESPONSES = {
    #1 pagina
    "holax": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
  
    #pagina de registro
    "cotizacion": {"body": bot.nameandnumber["message"]},
    "mantenimiento": {"body": bot.nameandnumber["message"]},
    
    #2 pagina
    "cotizar": {"question": bot.cotizacion["message"], "options": bot.cotizacion["option"], "list": "on"},
    "citaManteni": {"body": bot.mantenimientoMens["message"]},
  
    #3 pagina
    "on grid": {"question": bot.cotizacion_grid["message"], "options": bot.cotizacion_grid["option"]},
    "off grid": {"question": bot.cotizacion_offgrid["message"], "options": bot.cotizacion_offgrid["option"]},
    "sistema hibrido": {"body": bot.cotizacion_hibrido["message"], "question": bot.cotizacion_hibrido["question"], "options":bot.cotizacion_hibrido["option"], "media": ("consumo", "image")},
    
    #4 pagina on-grid
    "residencial": {"body": bot.Residencial_cotizar["message"], "question": bot.Residencial_cotizar["question"], "options": bot.Residencial_cotizar["option"], "media": ("consumo", "image")},
    "comercial": {"body": bot.Residencial_coti_comercial["message"], "question": bot.Residencial_coti_comercial["question"], "options": bot.Residencial_coti_comercial["option"], "media": ("consumo", "image")},
    "industrial": {"body": bot.Residencial_coti_mayor["message"], "contact": ("name", "number")},
    
    #4 pagina off-grid
    "sistemas aislados":{"body": bot.offgrid_pdf["message"], "media": ("catalogo", "documents"), "question":"¿Estas interesado? Agenda una cita", "options": ["Agendar cita 🗓️"]},
    "aire hibrido solar":{"body": bot.offgrid_pdf["message"], "media": ("aire_solar", "documents"), "question":"¿Estas interesado? Agenda una cita",  "options": ["Agendar cita 🗓️"]},
  
    #4 pagina hibrido y 5 on-grid
    "ahorro hasta": {"body": bot.Residencial_coti_pdf["message"], "media": ("cotizacion_", "documents"), "question":"¿Estas interesado? Agenda una cita", "options": ["Agendar cita 🗓️"]},

    
    "Ok, gracias": {"body": bot.Residencial_coti_mayor["message"], "contact": ("name", "number")},
    "agendar cita": {"body": bot.agendar["message"], "media": ("nic", "image")}
}

RESPONSE_IA = {
    "no estoy seguro": {"responseIA": "no estoy seguro sobre que tipo de sistema solar utilizar on grid o off grid","action": "text"},
    "desconozco estos temas": {"responseIA": "no tengo conociemientos de sistemas off grid, on grid o hibridos, podrias explicarme", "action": "cotizar"}
    
}

FOOTER = ""



def enviar_respuesta(number, text, messageId, response_data, conver):
    lista_respuestas = []

    if "media" in response_data:
        media_id, media_category = response_data["media"]
        lista_respuestas.append(enviar_media(number, media_id, media_category, response_data, text))
        conver.new_message("bot_Greengol", response_data.get("body", ""))

    if "body" in response_data and "media" not in response_data:
        lista_respuestas.append(text_Message(number, response_data["body"]))
        conver.new_message("bot_Greengol", response_data["body"])

    if "options" in response_data:
        reply = generar_botones(number, response_data, messageId)
        lista_respuestas.append(reply)
        conver.new_message("bot_Greengol", response_data["question"])

    if "contact" in response_data:
        name_id, number_id = response_data["contact"]
        lista_respuestas.append(contact_Message(number, sett.contact[name_id], sett.contact[number_id]))

    if "responseIA" in response_data:
        lista_respuestas.append(procesar_ia(number, text, response_data, messageId))

    return lista_respuestas


def enviar_media(number, media_id, media_category, response_data, text):
    if media_category == "image":
        return image_Message(number, get_media_id(media_id, media_category), response_data["body"])
    if media_category == "documents":
        if "cotizacion_" in media_id:
            return document_Message(number, sett.documents[f"cotizacion_{text[13:-3]}"], response_data["body"], f"Cotización {text[13:-3]} kwh.pdf")
        return document_Message(number, sett.documents[media_id], response_data["body"], f"{media_id.capitalize().replace('_', ' ')}.pdf")


def generar_botones(number, response_data, messageId):
    if "list" in response_data:
        return listReply_Message(number, response_data["options"], response_data["question"], FOOTER, "sed1", messageId)
    return buttonReply_Message(number, response_data["options"], response_data["question"], FOOTER, "sed1", messageId)


def procesar_ia(number, text, response_data, messageId):
    respuesta_ia = ia.Request(response_data["responseIA"])
    if response_data.get("action") == "cotizar":
        return buttonReply_Message(number, ["Cotizar"], f"{respuesta_ia}\n\n*Puedes seguir tu cotización presionando el botón*", FOOTER, "sed2", messageId)
    return text_Message(number, respuesta_ia)


def recorrer(responses_dict, number, text, messageId, conver):
    for keyword, response_data in responses_dict.items():
        if keyword in text:
            return enviar_respuesta(number, text, messageId, response_data, conver)
    return None


def IAresponse(text, number, messageId, name, conver):
    list_ia = recorrer(RESPONSE_IA, number, text, messageId, conver)
    if list_ia:
        for item in list_ia:
            enviar_Mensaje_whatsapp(item)
            time.sleep(1)
    else:
        procesar_respuesta_general(text, number, messageId, name, conver)

def verificar_ia(text, respuesta_ia, number, name, messageId, conver):
    def enviar_solicitud(hist, tipo_solicitud):
        nombre, correo, telefono = history.user_info(number)
        messageUs = hist[0]["mensajes"][-1]["mensaje"]
        destinatario, asunto, mensaje, foter = sendemail.loadcorreox(nombre, correo, telefono, messageUs)
        sendemail.enviar_correo(destinatario, asunto, mensaje, foter, number)
        
        soli_env = "Solicitud enviada ✅\n\n"
        return (
            buttonReply_Message(number, ["Volver a cotizar"], soli_env + tipo_solicitud, FOOTER, "sed1", messageId),
            soli_env + tipo_solicitud,
        )

    botoninf = "\n\n*Si quieres Iniciar una cotización presiona el botón.*"
    hist = history.historialwrite(name, -6)
    
    # Casos específicos de respuesta IA
    acciones_ia = {
        "registrogreen": lambda: (
            buttonReply_Message(number, ["Cotizar"], f"Fue registrado satisfactoriamente ✅\n\n{respuesta_ia[:-13]}{botoninf}", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
        "agendarbot": lambda: (
            buttonReply_Message(number, ["Cotizar"], f"{respuesta_ia[:-7]} Presionando el botón", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
        "greengloduda": lambda: (
            text_Message(number, respuesta_ia[:-12]),
            respuesta_ia[:-12],
        ),
        "cotigreenglo": lambda: (
            buttonReply_Message(number, ["Cotizar"], f"{respuesta_ia[:-12]}{botoninf}", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
        "greenInforma": lambda: (
            buttonReply_Message(number, bot.welcome["option"], f"{respuesta_ia[:-12]}{botoninf}", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
        "greenhola": lambda: (
            buttonReply_Message(number, ["Iniciar ✅"], f"{respuesta_ia[:-9]}\n\n*Si quieres Iniciar una cotización o otro servicio presiona el botón.*", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
        "asesorgreen": lambda: (
            buttonReply_Message(number, ["Agendar cita 🗓️"], f"{respuesta_ia[:-11]}\n\n*Para agendar una cita presiona el botón.*", FOOTER, "sed1", messageId),
            respuesta_ia
        ),
    }

    # Lógica para manejar casos específicos
    if "greenglo visita" in respuesta_ia or (hist[0]["mensajes"][-2]["mensaje"] in bot.agendar["message"] and "cotizacion" in respuesta_ia):
        if history.historialread(hist, "mantenimiento "):
            return enviar_solicitud(hist, "Un asesor de greenglo se estará comunicando con usted lo más pronto posible.")
        if history.historialread(hist, "agendar cita "):
            tipo_respuesta = respuesta_ia[:-15] if "greenglo visita" in respuesta_ia else respuesta_ia[:-31]
            return enviar_solicitud(hist, tipo_respuesta)
    
    # Lógica basada en claves de respuesta IA
    for key, action in acciones_ia.items():
        if key in respuesta_ia:
            return action()

    # Caso por defecto
    respuesta_ia = bot.Nomessage["message"]
    return buttonReply_Message(number, bot.welcome["option"], respuesta_ia, FOOTER, "sed1", messageId), respuesta_ia


def procesar_respuesta_general(text, number, messageId, name, conver):
    respuesta_ia = ia.Request(text)
    formatIA, respuestaIA = verificar_ia(text, respuesta_ia, number, name,messageId, conver)
    conver.new_message("bot_Greengol", respuestaIA)
    enviar_Mensaje_whatsapp(formatIA)


def administrar_chatbot(text, number, messageId, name):
    if text in ["iniciar ✅", "volver al inicio ✅"]: 
        text = "Holax"
    
    text = unidecode(text.lower())
    conver = database.Conversacion(number, messageId, name)

    if not conver.check_User():
        conver.new_user()
    conver.new_message("usuario", text)

    if "cotizacion" in text: 
        text = "cotizar" if conver.check_user_info() else "cotizacion" 
    elif "mantenimiento" == text and conver.check_user_info(): 
        text = "citaManteni"
      
    enviar_Mensaje_whatsapp(markRead_Message(messageId))
    time.sleep(1)

    lista_respuestas = recorrer(RESPONSES, number, text, messageId, conver)
    if "mensaje no procesado" not in text:
      if lista_respuestas:
        for respuesta in lista_respuestas:
            enviar_Mensaje_whatsapp(respuesta)
            time.sleep(1)
      else:
          IAresponse(text, number, messageId, name, conver)
    else:
      enviar_Mensaje_whatsapp(buttonReply_Message(number, bot.welcome["option"], bot.Notype["message"], FOOTER, "sed1", messageId))