import os
import time
import requests


class Metabase(object):

    def __init__(self, *args, endpoint=None, email=None,
                 password=None, session=None, **kwargs):
        self.endpoint = endpoint or os.getenv('METABASE_ENDPOINT') + '/api'
        self.email = email or os.getenv('METABASE_AUTH_EMAIL')
        self.password = password or os.getenv('METABASE_AUTH_PASSWORD')
        self.session = session or os.getenv('METABASE_SESSION')
        self.auth_callback = kwargs.pop('auth_callback', None)

        if self.session is None:
            self.auth()

    def session_header(self):
        return {'X-Metabase-Session': self.session}

    def get_session_headers(self, *args, **kwargs):
        res = requests.get(self.endpoint + '/user/current',
                           headers=self.session_header())
        if res.status_code == 401:
            self.auth()
        return self.session_header()

    def fetch_header(self, r):
        if r.status_code == 200:
            return True
        else:
            return False

    def fetch_body(self, r):
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, None

    def _get_session_headers(self, kwargs):
        if not kwargs.pop('check_session', True):
            return self.get_session_header(**kwargs)
        return headers or {}

    def get(self, *args, headers=None, **kwargs):
        headers = self.get_session_headers(headers, kwargs)
        r = requests.get(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def post(self, *args, headers=None, **kwargs):
        headers = self.get_session_headers(headers, kwargs)
        r = requests.post(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def put(self, *args, headers=None, **kwargs):
        headers = self.get_session_headers(headers, kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def delete(self, *args, headers=None, **kwargs):
        headers = self.get_session_headers(headers, kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def auth(self, **kwargs):
        payload = {
            'username': self.email,
            'password': self.password
        }

        res = requests.post(self.endpoint + '/session', json=payload)

        if res.status_code == 200:
            data = res.json()
            self.session = data['id']
        else:
            raise Exception(res)

        if hasattr(self, 'auth_callback') and callable(self.auth_callback):
            self.auth_callback(self)
