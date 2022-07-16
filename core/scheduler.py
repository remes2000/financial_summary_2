from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core import env, nordigen, database

def init():
    scheduler = BlockingScheduler()
    fetch_data()
    scheduler.add_job(fetch_data, 'interval', seconds=env.FETCH_INTERVAL_IN_SECONDS)
    scheduler.start()

def fetch_data():
    accounts = nordigen.session.get_accounts()
    transactions = nordigen.session.get_transactions(accounts)
    database.insert_transactions(transactions)