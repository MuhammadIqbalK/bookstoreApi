from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


# class ini akan memodifikasi pesan exeption milik primaryKeyRelatedField
class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        self.resource_name = kwargs.pop('resource_name', None)
        super().__init__(*args, **kwargs)
    
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except ObjectDoesNotExist:
            raise ValidationError(f"{self.resource_name} with id {data} does not exist.")
        except serializers.ValidationError as exc:
            raise ValidationError(f"{self.resource_name} with id {data} does not exist.")
