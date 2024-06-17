from django.db import models
from random import randint

def generate_unique_big_integer():
    return randint(100000001, 999999999) 

class UniqueBigIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', generate_unique_big_integer)
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'BIGINT'

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value
        return int(value)

    def get_prep_value(self, value):
        return int(value) if value is not None else None
