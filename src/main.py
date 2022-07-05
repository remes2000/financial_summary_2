import os
import database
import scheduler
from nordigen import NordigenSession

NORDIGEN_ID = os.getenv('NORDIGEN_ID') or ''
NORDIGEN_SECRET = os.getenv('NORDIGEN_SECRET') or ''

def main():
    print('Initializing database...')
    database.init()
    print('Initializing scheduler...')
    scheduler.init()

main()