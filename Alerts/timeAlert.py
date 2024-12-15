from apscheduler.schedulers.background import BackgroundScheduler
import Alerts.alertUser as alertUser
import Alerts.answerUser as answerUser

def alerta3min():
    alertaMin = alertUser.Alerts()
    alertaMin.check_and_process_recordatory()

def alerta24hours():
    alertaHour = alertUser.Alerts()
    alertaHour.alertGeneral()
    
def iniciar_timers(): 
    scheduler = BackgroundScheduler()
    # alerta cada  minuto
    scheduler.add_job(answerUser.user, "interval", seconds=3)
    # alerta cada 1 minuto
    scheduler.add_job(alerta3min, "interval", minutes=1)
    # alerta cada 48 horas
    scheduler.add_job(alerta24hours, "interval", minutes=10)
    scheduler.start()