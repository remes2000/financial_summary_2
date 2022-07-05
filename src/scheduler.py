from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

def init():
    scheduler = BlockingScheduler()
    fetch_data()
    scheduler.add_job(fetch_data, 'interval', seconds=10)
    scheduler.start()

def fetch_data():
    print('Fetching data...')