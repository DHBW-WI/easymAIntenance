from time import sleep
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from update_user import add_user, revoke_user


scheduler = BackgroundScheduler()                                                               # Initialisiert einen BackgroundScheduler und startet diesen
scheduler.start()

def get_j():                                                                                    # Gibt eine Liste der geplanten Aktionen (hinzufügen/entfernen der Nutzer) zurück
    scheduler.print_jobs()
    return str(scheduler.get_jobs(jobstore=any))

def add(name, ip):
    print(add_user(str(ip), str(name)))
 
def revoke(name):                                                                               # Ruft revoke_user auf. Der Nutzer wird aus der Berechtigungsgruppe entfernt
    print(revoke_user(str(name)))
    
def schedule_job(start, end, name, ip):
    start_o = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    if start_o < datetime.now():                                                                # Verhindert das Nutzen einer zurückliegenden Startzeit
        start = (datetime.now()+ timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%S")           # Startzeit wird in dem Fall immer auf den aktuellen Zeitpunkt gesetzt 
    scheduler.add_job(add, 'date', run_date=start, args=[name, ip])
    scheduler.add_job(revoke, 'date', run_date=end, args=[name])
    print("Success: ", start, end, name)
    return "Success"



