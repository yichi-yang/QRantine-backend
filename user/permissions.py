from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Record


class RecordOwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        assert isinstance(obj, Record), (
            'Expected a Record instance, got %s instead.' %
            (type(obj))
        )

        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        return False
