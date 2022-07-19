from shared.nordigen import NordigenSession
from simple_term_menu import TerminalMenu

def main():
    secret_id = input('SECRET_ID: ')
    secret_key = input('SECRET_KEY: ')
    session = NordigenSession(secret_id, secret_key)
    requisitions = list(map(lambda r: r['id'], session.get_requisitions()))
    print('Requisitions: ')
    print(requisitions)
    if input('Clear all requisitions? [Y/n]') == 'Y':
        clear_all_requisitions(session, requisitions)
        return
    if input('Clear one of requisitions? [Y/n]') == 'Y':
        print('Select requisition to clear')
        clear_requisition(session, requisitions[TerminalMenu(requisitions).show()])

def clear_all_requisitions(session, ids): 
    for id in ids:
        clear_requisition(session, id)

def clear_requisition(session, id):
    print('Deleting requisition: ' + id + '...')
    session.delete_requisition(id)

main()