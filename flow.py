from services import *
import textbot as bot
import sett
import database
import ia
import sendemail 
import history
import eraser
# Diccionario para almacenar los mensajes
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
    #"informacion": {"question": "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?", "options": ["Sobre nosotros", "Energia solar", "Contacto"]},
    "no, gracias.": {"body": "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊"}
}

response_IA = {
    "no estoy seguro": {"responseIA": "no estoy seguro sobre que tipo de sistema solar utilizar on grid o off grid"}
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
        if "list" in response_data:
          replyButtonData = listReply_Message(number, response_data["options"], response_data["question"], footer, "sed1", messageId)
        else:
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
        replytextIA = text_Message(number,answer_ia)
        list.append(replytextIA)

    return list

def recorrer(respont, number, text, messageId, conver):
    list = None
    for keyword in respont:
        if keyword in text:
            response_data = respont[keyword]
            list = enviar_respuesta(number, text, messageId, response_data, conver)
            continue
    return list

def IAresponse(text, number, messageId, name, conver):
    list_2 = recorrer(response_IA, number, text, messageId, conver)
    if list_2 :
        for item in list_2:
            enviar_Mensaje_whatsapp(item)
            time.sleep(1)
    else:
        print("fdfdf")
        answer_ia = ia.Request(text)
        if "greenglocotiza" in answer_ia:
            print("greenglocotiza")
            hist = history.historialwrite(name, -1)
            print(hist[0]["mensajes"][0]["mensaje"])
            nombre, correo, telefono, comentario = eraser.eraserx(hist[0]["mensajes"][0]["mensaje"])
            
            destinatario, asunto, mensaje, foter = sendemail.loadcorreo(nombre, correo, telefono, comentario)
            sendemail.enviar_correo(destinatario, asunto, mensaje, foter)
            enviar_Mensaje_whatsapp(text_Message(number,answer_ia))

        elif "cotizar" in answer_ia:
            print("ccccccc")
            hist = history.historialwrite(name, -4)
            authorization = history.historialread(hist,"agendar cita 🗓️")
            
            if authorization:
                
                destinatario = "hudaayy14@gmail.com"
                asunto = "Agenda cita"
                mensaje = text
                
                sendemail.enviar_correo(destinatario, asunto, mensaje)
                answer_ia = ia.Request(text+" estos son mis dato para agendar una cita con greenglo")
                enviar_Mensaje_whatsapp(text_Message(number,answer_ia))
            else:
                answer_ia = answer_ia[:-17]+"presiona Cotizar."
                print(answer_ia)
                print(number)
                replyButtonData = buttonReply_Message(number, ["Cotizar"], answer_ia, footer, "sed1", messageId)
                enviar_Mensaje_whatsapp(replyButtonData)
        else:    
            enviar_Mensaje_whatsapp(text_Message(number,answer_ia))
        conver.new_message("bot_Greengol",answer_ia)

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
        IAresponse(text, number, messageId, name, conver)