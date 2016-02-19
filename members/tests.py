from functools import wraps
from unittest.mock import patch
from django.test import TestCase
from . import factories


def mock_entrecles_login(func):
    class FakeResponse(object):
        status_code = 302
        headers = {'Location': '/Accueil.aspx'}
        text = '''<html><body><input id="__VIEWSTATE" value="">
                  <input id="__EVENTVALIDATION" value=""></body></html>'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        with patch('requests.sessions.Session.request', return_value=FakeResponse):
            return func(*args, **kwargs)
    return wrapper


class LoggedTestMixin(object):
    @mock_entrecles_login
    def setUp(self):
        adhesion = factories.AdhesionFactory.create()
        self.client.login(username=adhesion.person.number, password='toto')
        super().setUp()


class LoginTests(TestCase):
    def test_no_password(self):
        adhesion = factories.AdhesionFactory.create()
        self.assertFalse(self.client.login(username=adhesion.person.number, password='toto'))

    def test_no_adhesion(self):
        person = factories.PersonFactory.create()
        self.assertFalse(self.client.login(username=person.number, password='toto'))

    @mock_entrecles_login
    def test_login(self):
        adhesion = factories.AdhesionFactory.create()
        logged = self.client.login(username=adhesion.person.number, password='toto')
        self.assertTrue(logged)
