import os
import time
import signal
import httplib
import subprocess


try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import pytest


TESTDIR = os.path.abspath(os.path.dirname(__file__))
SAMPLES = os.path.join(TESTDIR, 'sample_apps')


class TestClient:
    XHR = {'X-Requested-With': 'XMLHttpRequest'}

    def __init__(self, host='127.0.0.1', port=8080):
        self.conn = httplib.HTTPConnection(host, port, timeout=200)

    def request(self, method, url, body=None, headers={}):
        self.conn.connect()
        self.conn.request(method, url, body, headers)
        resp = self.conn.getresponse()
        self.conn.close()
        return resp

    def get(self, url, headers={}):
        return self.request('GET', url, headers=headers)

    def post(self, url, data={}, headers={}):
        return self.request('POST', url, body=urlencode(data), headers=headers)

    def delete(self, url, headers={}):
        return self.request('DELETE', url, headers=headers)

    def patch(self, url, data={}, headers={}):
        return self.request('PATCH', url, body=urlencode(data),
                            headers=headers)

    def put(self, url, data={}, headers={}):
        return self.request('PUT', url, body=urlencode(data), headers=headers)


class TestServer:
    def __init__(self):
        self.pid = None

    def start(self, path):
        app_path = os.path.join(SAMPLES, path)
        self.pid = subprocess.Popen(['/usr/bin/env', 'python', app_path]).pid
        time.sleep(0.5)

    def stop(self):
        if not self.pid:
            return
        os.kill(self.pid, signal.SIGTERM)


@pytest.fixture
def http_client():
    return TestClient


@pytest.yield_fixture
def sample_app():
    server = TestServer()
    try:
        yield server.start
    finally:
        server.stop()
