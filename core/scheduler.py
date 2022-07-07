from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core import env, nordigen

def init():
    scheduler = BlockingScheduler()
    fetch_data()
    scheduler.add_job(fetch_data, 'interval', seconds=10)
    scheduler.start()

def fetch_data():
    accounts = nordigen.session.get_accounts()
    transactions = nordigen.session.get_transactions(accounts)
    print(transactions)
    