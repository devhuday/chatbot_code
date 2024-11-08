from services import *
import textbot as bot
import sett
import database
import ia

# Diccionario para almacenar los mensajes
responses = {
    "hola": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
    "cotizacion": {"question": bot.cotizacion_grid["message"], "options": bot.cotizacion_grid["option"]},
    "residencial": {"question": bot.Residencial["message"], "options": bot.Residencial["option"]},
    "me parece costoso": {"body": bot.Residencial_coti_mayor["message"]},
    "si, deseo cotizar": {"body": bot.Residencial_cotizar["message"], "question": bot.Residencial_cotizar["question"], "options": bot.Residencial_cotizar["option"], "media": ("consumo", "image")},
    "menor a 1000kwh": {"question": bot.Residencial_coti_menor["message"], "options": bot.Residencial_coti_menor["option"]},
    "entre 1000 y 2000kwh": {"question": bot.Residencial_coti_entre["message"], "options": bot.Residencial_coti_entre["option"]},
    "mayor a 2000kwh": {"body": bot.Residencial_coti_mayor["message"], "contact": ("name", "number")},
    "ahorro hasta": {"body": bot.Residencial_coti_pdf["message"], "media": ("cotizacion_", "documents")},
    "informacion": {"question": "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?", "options": ["Sobre nosotros", "la energia solar", "contacto"]},
    "no, gracias.": {"body": "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊"}
}

response_IA = {
    "no estoy seguro": {"responseIA": "no estoy seguro sobre que tipo de sistema solar utilizar on grid o off grid para mi plan de energia solar"}
}

footer = "Equipo Greenglo"

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
    
    if "contact" in response_data:
        name_id, number_id = response_data["contact"]
        replycontact = contact_Message(number,sett.contact[name_id],sett.contact[number_id])
        list.append(replycontact)
    
    if "responseIA" in response_data:
        general_prompt = response_data["responseIA"]
        answer_ia = ia.Request(general_prompt)
        replytext = text_Message(number,answer_ia)
        list.append(replytext)
        
    # Envía la reacción
    #replyReaction = replyReaction_Message(number, messageId, "🫡")
    #list.append(replyReaction)

    return list

def recorrer(number, text, messageId, conver):
    for keyword in responses:
        if keyword in text:
            response_data = responses[keyword]
            list = enviar_respuesta(number, text, messageId, response_data, conver)
            continue
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
    
    list = recorrer(responses,number, text, messageId, conver)
    if list :        
        for item in list:
            enviar_Mensaje_whatsapp(item)
            time.sleep(1)
    else:
        list_2 = recorrer(response_IA,number, text, messageId, conver)
        if list_2 :
            enviar_Mensaje_whatsapp(list_2)
        else:
            answer_ia = ia.Request(text)
            enviar_Mensaje_whatsapp(text_Message(number,answer_ia))
        conver.new_message("bot_Greengol",answer_ia)