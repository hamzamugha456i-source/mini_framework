from .validators import RequiredValidator

class ValidationMixin:
    def validate_data(self, data, rules):
        """
        rules = {'field_name': [Validator1(), Validator2()]}
        """
        errors = {}
        for field, validators in rules.items():
            value = data.get(field)
            for validator in validators:
                try:
                    validator.validate(value, field)
                except Exception as e:
                    if field not in errors:
                        errors[field] = []
                    errors[field].append(str(e))
        return errors