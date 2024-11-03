from services import *
import textbot as bot
import sett

# Diccionario para almacenar los mensajes
responses = {
    "hola": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
    "cotizacion": {"body": bot.cotizacion["message"], "options": bot.cotizacion["option"]},
    "residencial": {"body": bot.Residencial["message"], "options": bot.Residencial["option"]},
    "me parece costoso": {"body": bot.Residencial_coti_mayor["message"]},
    "si, deseo cotizar": {"body": bot.Residencial_cotizar["question"], "options": bot.Residencial_cotizar["option"], "media": ("consumo", "image")},
    "menor a 1000kwh": {"body": bot.Residencial_coti_menor["message"], "options": bot.Residencial_coti_menor["option"]},
    "entre 1000 y 2000kwh": {"body": bot.Residencial_coti_entre["message"], "options": bot.Residencial_coti_entre["option"]},
    "mayor a 2000kwh": {"body": bot.Residencial_coti_mayor["message"]},
    "ahorro hasta": {"body": bot.Residencial_coti_pdf["message"], "media": ("cotizacion_", "image")},
    "informacion": {"body": "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?", "options": ["Analítica Avanzada", "Migración Cloud", "Inteligencia de Negocio"], "media": ("perro_traje", "sticker")},
    "inteligencia de negocio": {"body": "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con una introducción a nuestros métodos de Inteligencia de Negocio?", "options": ["✅ Sí, envía el PDF.", "⛔ No, gracias"]},
    "sí, envía el pdf": {"body": "Genial, por favor espera un momento.", "media": ("pelfet", "sticker"), "document": sett.document_url},
    "sí, agenda reunión": {"body": "Estupendo. Por favor, selecciona una fecha y hora para la reunión:", "options": ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]},
    "7 de junio, 2:00 pm": {"body": "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?", "options": ["✅ Sí, por favor", "❌ No, gracias."]},
    "no, gracias.": {"body": "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊"}
}

#Declaramos algunas variables globales
footer = "Equipo Greengol"

def enviar_respuesta(number, text, messageId, response_data):
    list = []

    # Envía la imagen si existe
    if "media" in response_data:
        media_id, media_category = response_data["media"]
        if media_category == "images":
            enviar_Mensaje_whatsapp(image_Message(number, get_media_id(media_id,media_category), response_data["body"]))
        if media_category == "documents":
            media_id = media_id + text[13:-3]
            #document = document_Message(number, sett.documents[f"cotizacion_{text[13:-3]}"], "Listo 👍🏻", f"Cotización {text[13:-3]} kwh.pdf")
            enviar_Mensaje_whatsapp(document_Message(number,get_media_id(media_id,media_category), "Listo 👍🏻", f"Cotización {text[13:-3]} kwh.pdf"))
        time.sleep(1)  # Espera un segundo

    # Envía el texto
    if "body" in response_data and not ("media" in response_data):
        replytext = text_Message(number, response_data["body"])
        list.append(replytext)

    # Envía botones si existen
    if "options" in response_data:
        replyButtonData = buttonReply_Message(number, response_data["options"], response_data["question"], footer, "sed1", messageId)
        list.append(replyButtonData)

    # Envía la reacción
    #replyReaction = replyReaction_Message(number, messageId, "🫡")
    #list.append(replyReaction)

    return list


def administrar_chatbot(text, number, messageId, name):
    text = text.lower()
    list = []
    print("mensaje del usuario:", text)
    enviar_Mensaje_whatsapp(markRead_Message(messageId))
    time.sleep(1)
    
    for keyword in responses:
        if text in keyword:
            response_data = responses[keyword]
            list = enviar_respuesta(number, text, messageId, response_data)
            return list

    for item in list:
        enviar_Mensaje_whatsapp(item)
        time.sleep(1)



























def administrar_chatbot2(text,number, messageId, name):
    
    #mensaje que envio el usuario
    text = text.lower()
    list = []
    print("mensaje del usuario:",text)

    #primero marcamos como leido el mensaje del ususario
    markRead = markRead_Message(messageId)
    enviar_Mensaje_whatsapp(markRead)
    time.sleep(1)

    if "hola" in text:
        body = bot.welcome["question"]
        options = bot.welcome["option"]
        
        #enviamos el logo de primeras
        imagex = image_Message(number, get_media_id("welcome", "image"), bot.welcome["message"])
        enviar_Mensaje_whatsapp(imagex)
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "cotizacion" in text:
        body = bot.cotizacion["message"]
        options = bot.cotizacion["option"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
        
    elif "residencial" in text:
        body = bot.Residencial["message"]
        options = bot.Residencial["option"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
        
    elif "me parece costoso" in text:
        body = bot.Residencial_coti_costoso["message"]
        replytext = text_Message(number,body)
        list.append(replytext)
        
    elif "no deseo cotizar" in text:
        body = bot.Residencial_coti_negativa["message"]
        replytext = text_Message(number,body)
        list.append(replytext)
        
    elif "si, deseo cotizar" in text:
        
        #enviamos el logo de primeras
        imagex = image_Message(number, get_media_id("consumo", "image"), bot.Residencial_cotizar["message"])
        enviar_Mensaje_whatsapp(imagex)
        
        time.sleep(1)
        
        body = bot.Residencial_cotizar["question"]
        options = bot.Residencial_cotizar["option"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
    
    # hilo de cotizacion positiva
    elif "menor a 1000kwh" in text:
        body = bot.Residencial_coti_menor["message"]
        options = bot.Residencial_coti_menor["option"]
        replyButtonD = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonD)
        
    elif "entre 1000 y 2000kwh" in text:
        body = bot.Residencial_coti_entre["message"]
        options = bot.Residencial_coti_entre["option"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
    
    elif "mayor a 2000kwh" in text:
        body = bot.Residencial_coti_mayor["message"]
        replytext = text_Message(number,body)
        list.append(replytext)
        
    elif "ahorro hasta" in text:
        body = bot.Residencial_coti_pdf["message"]
        replytext = text_Message(number,body)
        list.append(replytext)
        time.sleep(2)

        document = document_Message(number, sett.documents[f"cotizacion_{text[13:-3]}"], "Listo 👍🏻", f"Cotización {text[13:-3]} kwh.pdf")
        enviar_Mensaje_whatsapp(document)
    
    
        
    elif "informacion" in text:
        body = "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?"
        options = ["Analítica Avanzada", "Migración Cloud", "Inteligencia de Negocio"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
        
    elif "inteligencia de negocio" in text:
        body = "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con una introducción a nuestros métodos de Inteligencia de Negocio?"
        options = ["✅ Sí, envía el PDF.", "⛔ No, gracias"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
        
    elif "sí, envía el pdf" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento.")

        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Listo 👍🏻", "Cotización.pdf")
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)

        body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
        options = ["✅ Sí, agenda reunión", "No, gracias." ]
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
        
    elif "sí, agenda reunión" in text :
        body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
        options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]

        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "7 de junio, 2:00 pm" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        options = ["✅ Sí, por favor", "❌ No, gracias."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "no, gracias." in text:
        textMessage = text_Message(number,"Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
    else :
        data = text_Message(number,"Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)
