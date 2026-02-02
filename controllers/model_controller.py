# controllers/model_controller.py
from .base import BaseController
from models.exceptions import ValidationError

class ModelController(BaseController):
    model = None  # Child classes must define this (e.g., model = User)

    def list(self):
        # GET /resource
        items = [item.to_dict() for item in self.model.all()]
        return self.json_response(items)

    def retrieve(self, id):
        # GET /resource/<id>
        item = self.model.get(id)
        if not item:
            return self.error_response('Item not found', '404 Not Found')
        return self.json_response(item.to_dict())

    def create(self):
        # POST /resource
        try:
            data = self.request.body
            if not data:
                return self.error_response("No data provided")
            
            # The model's save() method handles validation automatically
            instance = self.model.create(**data)
            return self.json_response(instance.to_dict(), '201 Created')
            
        except ValidationError as e:
            return self.error_response(str(e))
        except Exception as e:
            return self.error_response(str(e), '500 Internal Server Error')