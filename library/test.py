import database

number = 5519517
messageId = 11959595
name = "pedro"

conver=database.Conversacion(number,messageId,name)
if not conver.check_User():
    conver.new_user()
    
conver.new_message("usuario","textxddd22222d")