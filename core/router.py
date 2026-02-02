# core/router.py
import re

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, handler, methods=['GET']):
        # Convert path like /users/<id> to regex /users/(?P<id>[^/]+)
        pattern = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', path)
        self.routes.append({
            'pattern': re.compile(f'^{pattern}$'),
            'handler': handler,
            'methods': methods
        })

    def match(self, path, method):
        for route in self.routes:
            match = route['pattern'].match(path)
            if match and method in route['methods']:
                return route['handler'], match.groupdict()
        return None, None