# patterns/factory.py
from controllers.model_controller import ModelController

class ControllerFactory:
    @staticmethod
    def create_controller(model_class):
        """
        Dynamically creates a Controller class for a specific model
        """
        class DynamicController(ModelController):
            model = model_class
            
        return DynamicController