# validation/validators.py
from models.exceptions import ValidationError

class Validator:
    def validate(self, value, field_name):
        raise NotImplementedError

class RequiredValidator(Validator):
    def validate(self, value, field_name):
        if value is None or value == "":
            raise ValidationError(f"{field_name} is required")

class MaxLengthValidator(Validator):
    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self, value, field_name):
        if value and len(str(value)) > self.max_length:
            raise ValidationError(f"{field_name} cannot exceed {self.max_length} characters")