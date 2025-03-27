import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator:
    def __init__(self, message: str):
        self.message = message


    def __call__(self, value: str):
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(self.message)


@deconstructible
class PhoneValidator:
    def __init__(self, message: str):
        self.message = message


    def __call__(self, value: str):
        if not re.match(r'^\+359\d{9}', value):
            raise ValidationError(self.message)