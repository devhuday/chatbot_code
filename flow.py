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
responses = {
    #1 pagina
    "hola": {"body": bot.welcome["message"], "question": bot.welcome["question"], "options": bot.welcome["option"], "media": ("welcome", "image")},
  
    #pagina de registro
    "cotizacion": {"body": bot.nameandnumber["message"]},
    
    #2 pagina
    "cotizar": {"question": bot.cotizacion["message"], "options": bot.cotizacion["option"], "list": "on"},
    
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
    "agendar cita": {"body": bot.agendar["message"]}
}

response_IA = {
    "no estoy seguro": {"responseIA": "no estoy seguro sobre que tipo de sistema solar utilizar on grid o off grid","action": "text"},
    "desconozco estos temas": {"responseIA": "no tengo conociemientos de sistemas off grid, on grid o hibridos, podrias explicarme", "action": "cotizar"}
    
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
            elif "catalogo" in  media_id:
                mediax = document_Message(number, sett.documents[f"{media_id}"], response_data["body"], f"Catalogo Off grid.pdf")
            elif "aire_solar" in  media_id:
                mediax = document_Message(number, sett.documents[f"{media_id}"], response_data["body"], f"Aire solar.pdf")
            
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
        if "cotizar" in response_data["action"]:
          messagex = buttonReply_Message(number,["Cotizar"], f"{answer_ia} \n\n*Puedes seguir tu cotizacion presionando el boton*", footer, "sed2", messageId)
        else:
          messagex = text_Message(number,answer_ia)
        list.append(messagex)

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
        answer_ia = ia.Request(text)
        step = 6
        hist = history.historialwrite(name, -(step))
        if "greenglocotiza" in answer_ia:
            #hist = history.historialwrite(name, -1)
            if history.historialread(hist,"agendar cita "):
              messageUs = hist[0]["mensajes"][step-1]["mensaje"]
              print(messageUs)
              comentario = messageUs
              nombre, correo, telefono = history.user_info(number)
              print(nombre, correo, telefono)
              destinatario,asunto,mensaje,foter = sendemail.loadcorreox(nombre,correo,telefono,comentario)
              print("cargado")
              sendemail.enviar_correo(destinatario, asunto, mensaje, foter)
              answer_ia = "Solicitud enviada ✅"
              enviar_Mensaje_whatsapp(text_Message(number,answer_ia))

        elif "cotizar" in answer_ia:
            hist = history.historialwrite(name, -6)
            print("tiene cotizar")
            if history.historialread(hist,"agendar cita "):
                destinatario = "hudaayy14@gmail.com"
                asunto = "Agenda cita"
                mensaje = text
                
                sendemail.enviar_correo(destinatario, asunto, mensaje)
                answer_ia = ia.Request(text+" estos son mis dato para agendar una cita con greenglo")
                enviar_Mensaje_whatsapp(text_Message(number,answer_ia))
            
            elif history.historialread(hist,"cotizacion "):
                print("entra")
                if not conver.check_user_info():
                    print("entrax2")
                    num = history.historialmessages(hist,"cotizacion ")
                    print(num)
                    print(hist[0]["mensajes"][4]["mensaje"])
                    nombre, correo, telefono, comentario = eraser.eraserx(hist[0]["mensajes"][4]["mensaje"])
                    conver.new_userinfo(nombre, telefono, correo)
                    #enviar_Mensaje_whatsapp(text_Message(number,"Registrado satisfactoriamente ✅"))
                    #conver.new_message("bot_Greengol","Registrado satisfactoriamente ✅") 
                    answer_ia = "Registrado satisfactoriamente ✅\n\n"+answer_ia[:-17]+"presiona Cotizar."
                    print(answer_ia)
                    print(number)
                    replyButtonData = buttonReply_Message(number, ["Cotizar"], answer_ia, footer, "sed1", messageId)
                    enviar_Mensaje_whatsapp(replyButtonData)
            else:
                answer_ia = answer_ia[:-17]+"presiona Cotizar."
                print(answer_ia)
                print(number)
                replyButtonData = buttonReply_Message(number, ["Cotizar"], answer_ia, footer, "sed1", messageId)
                enviar_Mensaje_whatsapp(replyButtonData)
        elif "cotizacion" in answer_ia or "cotización" in answer_ia:
            answer_ia = answer_ia[:-20]+" presiona Cotizar."
            replyButtonData = buttonReply_Message(number, ["Cotizar"], answer_ia, footer, "sed1", messageId)
            enviar_Mensaje_whatsapp(replyButtonData)
        else:    
            enviar_Mensaje_whatsapp(text_Message(number,answer_ia))
    conver.new_message("bot_Greengol",answer_ia)

def administrar_chatbot(text, number, messageId, name):
    text = unidecode(text.lower())
    list = []
    print("mensaje del usuario:", text)
    
    conver = database.Conversacion(number,messageId,name)
    if not conver.check_User():
        conver.new_user()
    conver.new_message("usuario",text)   
    
    if "cotizacion" in text:
        if conver.check_user_info():
            text = "cotizar"
        
    
    enviar_Mensaje_whatsapp(markRead_Message(messageId))
    time.sleep(1)
    
    list = recorrer(responses,number, text, messageId, conver)
    if list :        
        for item in list:
            enviar_Mensaje_whatsapp(item)
            time.sleep(1)
    else:
        hist = history.historialwrite(name, -3)
        authorization = history.historialread(hist,bot.cotizacion_hibrido["message"])
        if authorization:
            print("se debe enviar correo")
            hist = history.historialwrite(name, -1)
            print(hist[0]["mensajes"][0]["mensaje"])
            nombre, correo, telefono, comentario = eraser.eraserx(hist[0]["mensajes"][0]["mensaje"])
            
            destinatario, asunto, mensaje, foter = sendemail.loadcorreo(nombre, correo, telefono, comentario)
            sendemail.enviar_correo(destinatario, asunto, mensaje, foter)
            enviar_Mensaje_whatsapp(text_Message(number,"solicitud enviada"))
        else:
            IAresponse(text, number, messageId, name, conver)