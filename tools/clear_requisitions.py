from shared.nordigen import NordigenSession

def main():
    secret_id = input('SECRET_ID: ')
    secret_key = input('SECRET_KEY: ')
    session = NordigenSession(secret_id, secret_key)
    requisitions = list(map(lambda r: r['id'], session.get_requisitions()))
    print('Requisitions: ')
    print(requisitions)
    if input('Clear all requisitions? [Y/n]') != 'Y':
        return
    for requisition in requisitions:
        print('Deleting requisition: ' + requisition + '...')
        session.delete_requisition(requisition)

main()