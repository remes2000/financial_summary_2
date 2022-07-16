import unittest
import requests_mock
import shared.nordigen as nordigen
from shared.nordigen import NordigenSessionManager

@requests_mock.Mocker()
class TestNordigenSessionManager(unittest.TestCase):
    def test_when_creating_manager_object_then_fetch_token(self, m):
        # given
        nordigen_id = 'id'
        nordigen_secret = 'secret'
        # when
        adapter = m.post(nordigen.NEW_TOKEN_URL, json={
            'access': 'TOKEN',
            'access_expires': 86400
        })
        manager = NordigenSessionManager(nordigen_id, nordigen_secret)
        # then
        self.assertEqual(adapter.call_count, 1)
        self.assertEqual(adapter.last_request.json(), {
            'secret_id': nordigen_id,
            'secret_key': nordigen_secret
        })
        

    def test_when_making_request_then_has_authorization_header(self, m):
        # given
        test_url = 'http://localhost/test'
        nordigen_token = 'TOKEN'
        # when
        m.post(nordigen.NEW_TOKEN_URL, json={
            'access': 'TOKEN',
            'access_expires': 86400
        })
        adapter = m.get(test_url)
        manager = NordigenSessionManager('id', 'secret')
        manager.get_session().get(test_url)
        # then
        self.assertEqual(adapter.last_request.headers['Authorization'], 'Bearer {}'.format(nordigen_token))

    def test_when_token_expired_and_get_session_then_fetch_token(self, m):
        # when
        m.post(nordigen.NEW_TOKEN_URL, json={
            'access': 'TOKEN',
            'access_expires': 0
        })
        manager = NordigenSessionManager('id', 'secret')
        adapter = m.post(nordigen.NEW_TOKEN_URL, json={
            'access': 'NEW_TOKEN',
            'access_expires': 86400
        })
        manager.get_session()
        # then
        self.assertEqual(adapter.call_count, 1)
        self.assertEqual(manager.token, 'NEW_TOKEN')