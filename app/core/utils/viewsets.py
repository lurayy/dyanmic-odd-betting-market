from builtins import AttributeError

from django.db.models import FileField, ImageField, TextField, JSONField
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db import transaction

EXCLUDE = [ImageField, FileField, TextField, JSONField]
EXCLUDE_FIELD_NAMES = ['password', 'is_superuser']


class DefaultViewSet(ModelViewSet):

    @property
    def ordering_fields(self):
        try:
            queryset = self.queryset if self.queryset else self.get_queryset()
            return [
                field.name for field in queryset.model._meta.fields if not any(
                    isinstance(field, e)
                    for e in EXCLUDE) and field.name not in EXCLUDE_FIELD_NAMES
            ]
        except AttributeError:
            return []

    @property
    def filterset_fields(self):
        try:
            queryset = self.queryset if self.queryset else self.get_queryset()
            return [
                field.name for field in queryset.model._meta.fields if not any(
                    isinstance(field, e)
                    for e in EXCLUDE) and field.name not in EXCLUDE_FIELD_NAMES
            ]
        except AttributeError:
            return []

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        hard_delete = request.GET.get('hardDelete', None)
        if hard_delete:
            with transaction.atomic():
                instance.delete()
            msg = 'Deleted successfully.'
        else:
            msg = 'Disabled successfully.'
            instance.is_active = False
            instance.save()
        return Response({'status': True, 'msg': msg})
