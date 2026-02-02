# patterns/repository.py
class Repository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.all()

    def get_by_id(self, id):
        return self.model.get(id)

    def create(self, data):
        return self.model.create(**data)