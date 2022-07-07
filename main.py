from core import database, nordigen, scheduler

def main():
    print('Initializing database...')
    database.init()
    print('Initializing nordigen session...')
    nordigen.init_session()
    print('Initializing scheduler...')
    scheduler.init()

main()