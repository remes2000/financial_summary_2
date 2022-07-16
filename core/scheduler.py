from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from core import env, nordigen, database
from core.models import AccountTransaction

def init():
    scheduler = BlockingScheduler()
    fetch_data()
    scheduler.add_job(fetch_data, 'interval', seconds=env.FETCH_INTERVAL_IN_SECONDS)
    scheduler.start()

def fetch_data():
    print('Fetching data...')
    accounts = nordigen.session.get_accounts()
    nordigen_transactions = nordigen.session.get_transactions(accounts)
    transactions = list(map(lambda t : AccountTransaction(nordigen_transaction=t), nordigen_transactions))
    categories = database.get_categories()
    for transaction in transactions:
        transaction.attach_category(categories)
    database.insert_transactions(transactions)
