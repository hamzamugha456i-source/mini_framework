# core/response.py
import json

class Response:
    def __init__(self, body='', status='200 OK', headers=None):
        self.body = body
        self.status = status
        self.headers = headers or [('Content-Type', 'text/plain')]

    def __call__(self, environ, start_response):
        start_response(self.status, self.headers)
        if isinstance(self.body, str):
            return [self.body.encode('utf-8')]
        return [self.body]

    @classmethod
    def json(cls, data, status='200 OK'):
        body = json.dumps(data)
        headers = [('Content-Type', 'application/json')]
        return cls(body, status, headers)

    @classmethod
    def text(cls, text, status='200 OK'):
        return cls(text, status, [('Content-Type', 'text/plain')])