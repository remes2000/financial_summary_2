import requests

NEW_TOKEN_URL = 'https://ob.nordigen.com/api/v2/token/new/'
CREATE_AGREEMENT_URL = 'https://ob.nordigen.com/api/v2/agreements/enduser/'
REQUISITION_URL = 'https://ob.nordigen.com/api/v2/requisitions/'
REDIRECT_URL = 'about:blank'

class NordigenSession:
    session = None
    secret_id = None
    secret_key = None

    def __init__(self, secret_id, secret_key):
        self.session = requests.Session()
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.fetch_token()
    
    def fetch_token(self):
        response = self.session.post(url = NEW_TOKEN_URL, data = {
            'secret_id': self.secret_id,
            'secret_key': self.secret_key
        })
        response.raise_for_status()
        self.token = response.json()['access']
        self.session.headers['Authorization'] = 'Bearer {}'.format(self.token)

    def create_agreement(self, institution_id, max_historical_days = 3, access_valid_for_days = 90):
        response = self.session.post(url = CREATE_AGREEMENT_URL, data = {
            'institution_id': institution_id,
            'max_historical_days': max_historical_days,
            'access_valid_for_days': access_valid_for_days,
            'access_scope': ['transactions']
        })
        response.raise_for_status()
        return response.json()['id']

    def create_agreement_url(self, institution_id, agreement_id):
        response = self.session.post(url = REQUISITION_URL, data = {
            'redirect': REDIRECT_URL,
            'institution_id': institution_id,
            'agreement': agreement_id,
            'user_language': 'EN'
        })
        response.raise_for_status()
        return response.json()['link']