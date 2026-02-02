# models/fields.py
from datetime import datetime
from .exceptions import ValidationError

class Field:
    def __init__(self, required=False, default=None):
        self.required = required
        self.default = default
        self.name = None  # Will be set by Model

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError(f"{self.name} is required")
        return value

class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def validate(self, value):
        super().validate(value)
        if value is not None and not isinstance(value, str):
             raise ValidationError(f"{self.name} must be a string")
        if value is not None and len(value) > self.max_length:
            raise ValidationError(f"{self.name} cannot exceed {self.max_length} chars")

class IntegerField(Field):
    def validate(self, value):
        super().validate(value)
        if value is not None and not isinstance(value, int):
            raise ValidationError(f"{self.name} must be an integer")

class DateTimeField(Field):
    def __init__(self, auto_now=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_now = auto_now

    def validate(self, value):
        if value is not None and not isinstance(value, datetime):
             raise ValidationError(f"{self.name} must be a datetime object")