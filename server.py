from flask import Flask, request
import sett 
import services
import flow
from apscheduler.schedulers.background import BackgroundScheduler
import alertUser
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
        #type = message['type']
        print(type)
        text = services.obtener_Mensaje_whatsapp(message)
        flow.administrar_chatbot(text, number,messageId,name)
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)

def alerta3min():
    alertaMin = alertUser.Alerts()
    alertaMin.check_and_process_recordatory()

def alerta24hours():
    alertaHour = alertUser.Alerts()
    alertaHour.alertGeneral()
    
def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    # alerta cada 1 minuto
    scheduler.add_job(alerta3min, "interval", minutes=2)
    # alerta cada 48 horas
    scheduler.add_job(alerta24hours, "interval", minutes=1)
    scheduler.start()

 
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    app.run()
