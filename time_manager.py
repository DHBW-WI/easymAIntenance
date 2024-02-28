from time import sleep
from apscheduler.schedulers.blocking import *
import datetime as dt
from update_user import add_user, revoke_user

scheduler = BlockingScheduler()


def add(name):
    print(add_user("remote_maintenance", str(name)))

def revoke(name):
    print(revoke_user(str(name)))
    scheduler.shutdown()

def schedule_job(start, end, name):
    scheduler.start()
    scheduler.add_job(add, 'date', run_date=start, args=[name])
    scheduler.add_job(revoke, 'date', run_date=end, args=[name])
    print("Success: ", start, end, name)
    return "Success"
    

#schedule_job("2024-02-16T15:42:00", "2024-02-16T15:46:30", "lukas_richter")

    
print(dt.datetime.now())