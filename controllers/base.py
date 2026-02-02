# controllers/base.py
from core.response import Response

class BaseController:
    def __init__(self, request):
        self.request = request

    def json_response(self, data, status='200 OK'):
        return Response.json(data, status=status)

    def text_response(self, text, status='200 OK'):
        return Response.text(text, status=status)
        
    def error_response(self, message, status='400 Bad Request'):
        return self.json_response({'error': message}, status=status)