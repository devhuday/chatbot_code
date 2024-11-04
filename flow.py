from services import *
import textbot as bot
import sett
import database

# Diccionario para almacenar los mensajes
responses = {
    "hola": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
    "cotizacion": {"question": bot.cotizacion["message"], "options": bot.cotizacion["option"]},
    "residencial": {"question": bot.Residencial["message"], "options": bot.Residencial["option"]},
    "me parece costoso": {"body": bot.Residencial_coti_mayor["message"]},
    "si, deseo cotizar": {"body": bot.Residencial_cotizar["message"], "question": bot.Residencial_cotizar["question"], "options": bot.Residencial_cotizar["option"], "media": ("consumo", "image")},
    "menor a 1000kwh": {"question": bot.Residencial_coti_menor["message"], "options": bot.Residencial_coti_menor["option"]},
    "entre 1000 y 2000kwh": {"question": bot.Residencial_coti_entre["message"], "options": bot.Residencial_coti_entre["option"]},
    "mayor a 2000kwh": {"body": bot.Residencial_coti_mayor["message"]},
    "ahorro hasta": {"body": bot.Residencial_coti_pdf["message"], "media": ("cotizacion_", "documents")},
    "informacion": {"body": "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?", "options": ["Analítica Avanzada", "Migración Cloud", "Inteligencia de Negocio"], "media": ("perro_traje", "sticker")},
    "inteligencia de negocio": {"body": "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con una introducción a nuestros métodos de Inteligencia de Negocio?", "options": ["✅ Sí, envía el PDF.", "⛔ No, gracias"]},
    "sí, envía el pdf": {"body": "Genial, por favor espera un momento.", "media": ("pelfet", "sticker"), "media": ("cotizacion_1300", "documents")},
    "sí, agenda reunión": {"body": "Estupendo. Por favor, selecciona una fecha y hora para la reunión:", "options": ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]},
    "7 de junio, 2:00 pm": {"body": "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?", "options": ["✅ Sí, por favor", "❌ No, gracias."]},
    "no, gracias.": {"body": "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊"}
}

footer = "Equipo Greengol"

def enviar_respuesta(number, text, messageId, response_data, conver):
    list = []
    print(response_data)
    
    # Envía la imagen 
    if "media" in response_data:
        media_id, media_category = response_data["media"]
        if media_category == "image":
            mediax = image_Message(number, get_media_id(media_id, media_category), response_data["body"])
        if media_category == "documents":
            if "cotizacion_" in media_id:
                media_id = media_id + text[13:-3]
            mediax = document_Message(number, sett.documents[f"cotizacion_{text[13:-3]}"], response_data["body"], f"Cotización {text[13:-3]} kwh.pdf")
        list.append(mediax)
        conver.new_message("bot_Greengol",response_data["body"]) 

    # Envía el texto
    if "body" in response_data and not ("media" in response_data):
        replytext = text_Message(number, response_data["body"])
        conver.new_message("bot_Greengol",response_data["body"]) 
        list.append(replytext)

    # Envía botones 
    if "options" in response_data:
        replyButtonData = buttonReply_Message(number, response_data["options"], response_data["question"], footer, "sed1", messageId)
        conver.new_message("bot_Greengol",response_data["question"])
        list.append(replyButtonData)

    # Envía la reacción
    #replyReaction = replyReaction_Message(number, messageId, "🫡")
    #list.append(replyReaction)

    return list

def administrar_chatbot(text, number, messageId, name):
    text = text.lower()
    list = []
    print("mensaje del usuario:", text)
    
    conver = database.Conversacion(number,messageId,name)
    if not conver.check_User():
        conver.new_user()
    conver.new_message("usuario",text)   
    
    enviar_Mensaje_whatsapp(markRead_Message(messageId))
    time.sleep(1)
    
    for keyword in responses:
        if keyword in text:
            response_data = responses[keyword]
            list = enviar_respuesta(number, text, messageId, response_data, conver)
            continue
    if list :        
        for item in list:
            enviar_Mensaje_whatsapp(item)
            time.sleep(1)
    else:
        print("no entendi nada")