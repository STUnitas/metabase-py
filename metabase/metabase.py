import os
import time
import requests

class Metabase():
    def __init__(self, *args, endpoint='http://localhost:3000', email=None, password=None, reauth_duration=7200, **kwargs):
        self.endpoint = endpoint + "/api"
        self.email = email
        self.password = password
        self.reauth_duration = reauth_duration

        self.session = None
        self.session_start = time.time()

        # get environment
        if self.email == None and os.environ['METABASE_AUTH_EMAIL'] != None:
            self.email = os.environ['METABASE_AUTH_EMAIL']
        if self.password == None and os.environ['METABASE_AUTH_PASSWORD'] != None:
            self.password = os.environ['METABASE_AUTH_PASSWORD']
        if self.endpoint != "http://localhost:3000" and os.environ['METABASE_ENDPOINT'] != None:
            self.endpoint = os.environ['METABASE_ENDPOINT']

        if self.session == None:
            self.auth()

    def check_session(self):
        now = int(time.time())
        if now - self.session_start > self.reauth_duration:
            self.auth()
        return {
                "X-Metabase-Session": self.session }

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

    def get(self, *args, **kwargs):
        headers = self.check_session()
        r = requests.get(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def post(self, *args, **kwargs):
        headers = self.check_session()
        r = requests.post(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def put(self, *args, **kwargs):
        headers = self.check_session()
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def delete(self, *args, **kwargs):
        headers = self.check_session()
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def auth(self):
        payload = {
                'email': self.email,
                'password': self.password}

        res, data = self.post("/session", json=payload)

        if res == True:
            self.session = data['id']
            self.session_start = int(time.time())
