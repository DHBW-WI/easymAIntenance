from time import sleep
from apscheduler.schedulers.background import *
#from datetime import datetime
from update_user import add_user, revoke_user

scheduler = BackgroundScheduler()

def add(name):
    print(add_user("remote_maintenance", str(name)))

def revoke(name):
    print(revoke_user(str(name)))

def schedule_job(start, end, name):
    scheduler.add_job(add, 'date', run_date=start, args=[name])
    scheduler.add_job(revoke, 'date', run_date=end, args=[name])
    

schedule_job("2024-02-16T15:42:00", "2024-02-16T15:46:30", "lukas_richter")
scheduler.start()

while True:
    sleep(1)