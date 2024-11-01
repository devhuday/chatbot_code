from services import *
import textbot as bot
import sett
#Declaramos algunas variables globales
footer = "Equipo Greengol"

def administrar_chatbot(text,number, messageId, name):
    
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
    
    elif "si, deseo cotizar" in text:
        
        #enviamos el logo de primeras
        imagex = image_Message(number, get_media_id("consumo", "image"), bot.Residencial_cotizar["message"])
        enviar_Mensaje_whatsapp(imagex)
        
        time.sleep(1)
        
        body = bot.Residencial_cotizar["question"]
        options = bot.Residencial_cotizar["option"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)
    
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

        document = document_Message(number, sett.documents[f"cotizacion_{text[13:-3]}"], "Listo 👍🏻", "Cotización.pdf")
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
