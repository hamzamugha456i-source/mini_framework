# models/base.py
from datetime import datetime
from .fields import Field, DateTimeField
from .exceptions import ValidationError

class Model:
    # Simulating a database: { ClassName: [instances...] }
    _storage = {}
    _id_counter = {}

    def __init__(self, **kwargs):
        self.id = None
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Set defaults for missing fields
        for name, field in self._get_fields().items():
            if name not in kwargs:
                setattr(self, name, field.default)

    @classmethod
    def _get_fields(cls):
        fields = {}
        for name, attr in cls.__dict__.items():
            if isinstance(attr, Field):
                fields[name] = attr
                attr.name = name # Tell the field what its name is
        return fields

    def save(self):
        self._validate()
        
        # Handle auto_now fields (like created_at)
        for name, field in self._get_fields().items():
            if isinstance(field, DateTimeField) and field.auto_now:
                if getattr(self, name) is None: # Only set if empty
                    setattr(self, name, datetime.now())

        cls = self.__class__
        # Initialize storage for this class if missing
        if cls not in Model._storage:
            Model._storage[cls] = []
            Model._id_counter[cls] = 1

        if self.id is None:
            self.id = Model._id_counter[cls]
            Model._id_counter[cls] += 1
            Model._storage[cls].append(self)
        else:
            # Update existing record
            existing_idx = next((i for i, obj in enumerate(Model._storage[cls]) if obj.id == self.id), -1)
            if existing_idx != -1:
                Model._storage[cls][existing_idx] = self

    def _validate(self):
        for name, field in self._get_fields().items():
            value = getattr(self, name, None)
            field.validate(value)

    def to_dict(self):
        data = {'id': self.id}
        for name in self._get_fields():
            value = getattr(self, name, None)
            if isinstance(value, datetime):
                value = value.isoformat()
            data[name] = value
        return data

    @classmethod
    def all(cls):
        return cls._storage.get(cls, [])

    @classmethod
    def get(cls, id):
        objects = cls.all()
        for obj in objects:
            if obj.id == int(id):
                return obj
        return None

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj
    
    @classmethod
    def filter(cls, **kwargs):
        # Requirements: Query methods (filter()) 
        objects = cls.all()
        results = []
        for obj in objects:
            match = True
            for key, value in kwargs.items():
                if getattr(obj, key, None) != value:
                    match = False
                    break
            if match:
                results.append(obj)
        return results