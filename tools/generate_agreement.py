from simple_term_menu import TerminalMenu
from shared.nordigen import NordigenSession

INSTITUTIONS = [
    'SANTANDER_PL_WBKPPLPP',
    'SANTANDER_PL_CORP_WBKPPLPP',
    'REVOLUT_REVOGB21'
]

class AgreementGenerator:
    nordigen = None

    def __init__(self, secret_id, secret_key):
        self.nordigen = NordigenSession(secret_id, secret_key)

    def generate(self, institution_id, max_historical_days, access_valid_for_day):
        agreement_id = self.nordigen.create_agreement(institution_id, max_historical_days, access_valid_for_day)
        return self.nordigen.create_agreement_url(institution_id, agreement_id)


def main():
    secret_id = input('SECRET_ID: ')
    secret_key = input('SECRET_KEY: ')
    max_historical_days = input('max_historical_days (3): ')
    access_valid_for_day = input('access_valid_for_day (90): ')
    institution_id = INSTITUTIONS[TerminalMenu(INSTITUTIONS).show()]
    print('INSTITUTION_ID: {}'.format(institution_id))
    agreement = AgreementGenerator(secret_id, secret_key).generate(institution_id, max_historical_days, access_valid_for_day)
    print('Agreement url: {} Id: {}'.format(agreement.link, agreement.id))
    
main()