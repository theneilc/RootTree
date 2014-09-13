from rest_framework import viewsets
from django.db import models
import uuid
from django.shortcuts import get_object_or_404


class UUIDLookupViewSetMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        filter = {'uuid': self.kwargs['pk']}
        # pk is actually the uuid

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UserModelMixin(models.Model):
    def create_user(self, email, password):
        User.objects.create_user(
            username=email,
            password=password,
            email=email
        )
        return user

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = uuid.uuid4().hex
        super(UUIDModelMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
