import base64
import hmac, hashlib
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from datetime import datetime
from core_roottree.mixins import *


DEFAULT_POLL_TIME = datetime(1901,1,1)

def build_absolute_uri(path, request=None):
    if request:
        host = request.META['HTTP_ORIGIN']
        return '%s%s' % (host, path)
    else:
        return settings.ABSOLUTE_URL_ROOT + path


class ClientUser(UserModelMixin, UUIDModelMixin):
    uuid = models.CharField(max_length=32, unique=True)
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User)
    lastpolltime = models.DateTimeField(default=DEFAULT_POLL_TIME)


class Developer(UserModelMixin, UUIDModelMixin):
    # email = models.EmailField(unique=True, max_length=254)
    uuid = models.CharField(max_length=32, unique=True)
    user = models.OneToOneField(User)


class Session(TimeStampedModel, UUIDModelMixin):
    uuid = models.CharField(max_length=32, unique=True)
    client = models.ForeignKey(ClientUser)
    developer = models.ForeignKey(Developer)

    STATUS_CHOICES = (
        (u'N', u'Not Requested'),
        (u'P', u'Pending'),
        (u'C', u'Completed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    result = models.TextField(null=True, blank=True)
    # file_url, null=True
    # result_url, null=False
    callback_url = models.URLField(null=True, blank=True)
    commandinstance = models.ForeignKey('CommandInstance')

    def get_local_file_url(self, request=None):
        path = '/api/file/?s=%s' %s self.uuid
        return build_absolute_uri(path, request)

    def get_result(self, request=None):
        # reads the contents of the result_url and file_url and returns
        # prettified result
        if self.result_url:
            # to do: handle more involved kinds of return values
            content = self.result_url
            result = content.split('\n')
        else:
            result = None

        if self.file_url:
            url = self.get_local_file_url(request)
            return {
                'file': url,
                'result': result
            }
        else:
            return {
                'result': result
            }

    @property
    def s3_signature(self):
        AWS_SECRET_ACCESS_KEY = 'CVdcUQd3jQXmHK5aaq5yrfYR+tdfYrRMF7M4UVFV'
        policy_document = open('/client/policy_document.json', 'r').read()
        policy = base64.b64encode(policy_document)
        signature = base64.b64encode(hmac.new(AWS_SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())

        return [policy, signature]


class Service(TimeStampedModel):
    commandinstance = models.OneToOneField('CommandInstance', related_name='command_service')
    lastrun = models.DateTimeField()
    frequency = models.IntegerField()  # time to wait in seconds


class Task(TimeStampedModel):
    commandinstance = models.OneToOneField('CommandInstance', related_name='command_task')


class CommandInstance(models.Model):
    command = models.ForeignKey('Command')
    args = models.TextField()
    kwargs = models.TextField()
    stdin = models.TextField()


class Command(TimeStampedModel):
    name = models.CharField(max_length=50, default='Unnamed Command')
    code = models.TextField()
    owner = models.ForeignKey(Developer, null=True, blank=True)
    LANGUAGE_CHOICES = (
        (u'b', u'bash'),
        (u'p', u'python'),
    )
    language = models.CharField(max_length=1, default='b')
    expectfile = models.BooleanField(default=False)


class Permission(TimeStampedModel):
    developer = models.ForeignKey(Developer)
    client = models.ForeignKey(ClientUser)
    command = models.ForeignKey(Command)
