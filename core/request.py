# core/request.py
import json

class Request:
    def __init__(self, environ):
        self.environ = environ
        self._method = environ.get('REQUEST_METHOD', 'GET')
        self._path = environ.get('PATH_INFO', '/')
        self._body = self._read_body()
        self._query_params = self._parse_query_params()
    
    def _read_body(self):
        try:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            if content_length > 0:
                body_bytes = self.environ['wsgi.input'].read(content_length)
                return json.loads(body_bytes)
        except (ValueError, KeyError):
            pass
        return {}

    def _parse_query_params(self):
        # Basic parsing (can be expanded)
        from urllib.parse import parse_qs
        qs = self.environ.get('QUERY_STRING', '')
        return {k: v[0] for k, v in parse_qs(qs).items()}

    @property
    def method(self):
        return self._method

    @property
    def path(self):
        return self._path

    @property
    def body(self):
        return self._body