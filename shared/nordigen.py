import requests
from datetime import date, datetime

NEW_TOKEN_URL = 'https://ob.nordigen.com/api/v2/token/new/'
REFRESH_TOKEN_URL = 'https://ob.nordigen.com/api/v2/token/refresh/'
CREATE_AGREEMENT_URL = 'https://ob.nordigen.com/api/v2/agreements/enduser/'
REQUISITION_URL = 'https://ob.nordigen.com/api/v2/requisitions/'
DELETE_REQUISITION_URL = 'https://ob.nordigen.com/api/v2/requisitions/{}'
TRANSACTION_URL = 'https://ob.nordigen.com/api/v2/accounts/{}/transactions/'
REDIRECT_URL = 'https://nieruchalski.pl'

class NordigenSession:
    manager = None

    def __init__(self, secret_id, secret_key):
        self.manager = NordigenSessionManager(secret_id, secret_key)

    def get_session(self):
        return self.manager.get_session()

    def create_agreement(self, institution_id, max_historical_days = 14, access_valid_for_days = 3):
        response = self.get_session().post(url = CREATE_AGREEMENT_URL, json = {
            'institution_id': institution_id,
            'max_historical_days': max_historical_days,
            'access_valid_for_days': access_valid_for_days,
            'access_scope': ['transactions']
        })
        response.raise_for_status()
        return response.json()['id']

    def create_agreement_url(self, institution_id, agreement_id):
        response = self.get_session().post(url = REQUISITION_URL, json = {
            'redirect': REDIRECT_URL,
            'institution_id': institution_id,
            'agreement': agreement_id,
            'user_language': 'EN'
        })
        response.raise_for_status()
        response_body = response.json()
        return NordigenAgreement(response_body['id'], response_body['link'])

    def get_requisitions(self):
        response = self.get_session().get(url = REQUISITION_URL)
        response.raise_for_status()
        return response.json()['results']

    def delete_requisition(self, id):
        response = self.get_session().delete(url = DELETE_REQUISITION_URL.format(id))
        response.raise_for_status()
    
    def get_accounts(self):
        accounts = []
        for requisition in self.get_requisitions():
            for account in requisition['accounts']:
                if account != '':
                    accounts.append(account)
        return accounts

    def get_transactions(self, accounts):
        transactions = []
        for account in accounts:
            response = self.get_session().get(
                    TRANSACTION_URL.format(account)
                )
            response.raise_for_status()
            for response_transaction in response.json()['transactions']['booked']:
                transactions.append(NordigenTransaction(response_transaction))
        return transactions

class NordigenSessionManager:
    EXPIRED_THRESHOLD = 30
    
    secret_id = None
    secret_key = None
    session = None
    token = None
    token_expires = None
    last_fetch_date = None

    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.session = requests.Session()
        self.fetch_token()
    
    def fetch_token(self):
        response = self.session.post(url = NEW_TOKEN_URL, json = {
            'secret_id': self.secret_id,
            'secret_key': self.secret_key
        })
        response.raise_for_status()
        response_body = response.json()
        self.last_fetch_date = datetime.now()
        self.token = response_body['access']
        self.token_expires = response_body['access_expires']
        self.session.headers['Authorization'] = 'Bearer {}'.format(self.token)

    def is_token_expired(self):
        return (self.token_expires - self.get_seconds_from(self.last_fetch_date)) <= self.EXPIRED_THRESHOLD

    def get_seconds_from(self, from_date):
        return int((datetime.now() - from_date).total_seconds())

    def get_session(self):
        if self.is_token_expired():
            self.fetch_token()
        return self.session


class NordigenAgreement:
    def __init__(self, id, link):
        self.id = id
        self.link = link

class NordigenTransaction:
    def __init__(self, response_body):
        self.id = response_body['transactionId']
        self.title = response_body['remittanceInformationUnstructured']
        amount_text = response_body['transactionAmount']['amount'].replace('.', '')
        self.amount = int(amount_text)
        self.date = response_body['valueDate']
        self.source = response_body
