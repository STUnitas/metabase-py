import os
import time
import requests

class Metabase():
    def __init__(self, *args, endpoint='http://localhost:3000', email=None, password=None, session=None, **kwargs):
        self.endpoint = endpoint
        self.email = email
        self.password = password
        self.session = session

        # get environment
        if self.email == None and os.getenv("METABASE_AUTH_EMAIL") != None:
            self.email = os.getenv("METABASE_AUTH_EMAIL")
        if self.password == None and os.getenv("METABASE_AUTH_PASSWORD") != None:
            self.password = os.getenv("METABASE_AUTH_PASSWORD")
        if self.endpoint == "http://localhost:3000" and os.getenv("METABASE_ENDPOINT") != None:
            self.endpoint = os.getenv("METABASE_ENDPOINT")
        if self.session == None and os.getenv("METABASE_SESSION") != None:
            self.session = os.getenv("METABASE_SESSION")

        self.endpoint = self.endpoint + "/api"

        if self.session == None:
            self.auth()

    def get_session_header(self, *args, **kwargs):
        res, _ = self.get("/user/current", check_session=False)
        if res == 401:
            self.auth()
        return { "X-Metabase-Session": self.session }

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

    def get(self, *args, headers={}, **kwargs):
        if kwargs.pop('check_session', True) != False:
            headers = self.get_session_header(**kwargs)
        r = requests.get(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def post(self, *args, headers={}, **kwargs):
        if kwargs.pop('check_session', True) != False:
            headers = self.get_session_header(**kwargs)
        r = requests.post(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def put(self, *args, headers={}, **kwargs):
        if kwargs.pop('check_session', True) != False:
            headers = self.get_session_header(**kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def delete(self, *args, headers={}, **kwargs):
        if kwargs.pop('check_session', True) != False:
            headers = self.get_session_header(**kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def auth(self, **kwargs):
        payload = {
                'email': self.email,
                'password': self.password}

        res, data = self.post("/session", json=payload)

        if res == True:
            self.session = data['id']

        auth_callback = kwargs.pop('auth_callback', None)
        if callable(auth_callback):
            auth_callback(self)
