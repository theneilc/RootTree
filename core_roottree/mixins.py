from rest_framework import viewsets


class CustomLookupViewSetMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UUIDLookupViewSetMixin(CustomLookupViewSetMixin):
    lookup_fields = ['uuid']
