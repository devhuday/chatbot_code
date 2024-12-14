from flask import Flask, request
import ChatFlow.sett as sett 
import ChatFlow.services as services
import MessageTools.flow as flow
from apscheduler.schedulers.background import BackgroundScheduler
import Alerts.timeAlert as alert
import Database.queue as queue

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    return 'Hola mundo'

@app.route("/testing", methods=["POST", "GET"])
def testing():
  print("Solicitud de UptimeRobot detectada.")
  return "recibida", 200

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        print(f"Se recibe:\n {body}")
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        type = message['type']
        print(type)
        text = services.obtener_Mensaje_whatsapp(message)
        services.enviar_Mensaje_whatsapp(services.markRead_Message(messageId))
        messageQueue = queue.verify_queue()
        if messageQueue:
            services.enviar_Mensaje_whatsapp(services.text_Message(number,"Espera un momento"))
        queue.load_message(messageQueue,name,number,messageId,text)
        return 'enviado'
    except Exception as e:
        return 'no enviado ' + str(e)
    
def test():
  print("enviarplantilla")
  plantilla=services.enviarplantilla("573058031242")
  services.enviar_Mensaje_whatsapp(plantilla)
 
if __name__ == '__main__':
    alert.iniciar_timers()
    app.run()
