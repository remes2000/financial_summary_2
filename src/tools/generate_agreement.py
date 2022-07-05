from simple_term_menu import TerminalMenu
from main.nordigen import Nordigen

INSTITUTIONS = [
    'SANTANDER_PL_WBKPPLPP',
    'SANTANDER_PL_CORP_WBKPPLPP',
    'REVOLUT_REVOGB21'
]

class AgreementGenerator:
    nordigen = None

    def __init__(self, secret_id, secret_key, institution_id):
        self.nordigen = Nordigen(secret_id, secret_key)

    def generate(self, institution_id):
        agreement_id = self.nordigen.create_agreement(institution_id)
        return self.nordigen.create_agreement_url(institution_id, agreement_id)


def main():
    secret_id = input('SECRET_ID: ')
    secret_key = input('SECRET_KEY: ')
    institution_id = INSTITUTIONS[TerminalMenu(INSTITUTIONS).show()]
    print('INSTITUTION_ID: {}'.format(institution_id))
    url = AgreementGenerator(secret_id, secret_key).generate(institution_id)
    print('Agreement url: {}'.format(url))
    
main()