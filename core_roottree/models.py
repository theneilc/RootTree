import base64
import hmac, hashlib, os
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from datetime import datetime
from core_roottree.mixins import *
from django.conf import settings


DEFAULT_POLL_TIME = datetime(1901,1,1)

def build_absolute_uri(path, request=None):
    if request:
        host = request.META['HTTP_ORIGIN']
        return '%s%s' % (host, path)
    else:
        return settings.ABSOLUTE_URL_ROOT + path


class CustomClientUserManager(models.Manager):
    def create_clientuser_from_user(self, user):
        self.model.objects.create(user=user)


class ClientUser(UserModelMixin, UUIDModelMixin):
    uuid = models.CharField(max_length=32, unique=True)
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User, related_name="related_clientuser")
    lastpolltime = models.DateTimeField(default=DEFAULT_POLL_TIME)
    objects = CustomClientUserManager()


class Developer(UserModelMixin, UUIDModelMixin):
    # email = models.EmailField(unique=True, max_length=254)
    uuid = models.CharField(max_length=32, unique=True)
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100, default='')
    url = models.URLField(null=True, blank=True)


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
    file_url = models.TextField(null=True, blank=True)
    result_url = models.TextField(null=True, blank=True)
    callback_url = models.URLField(null=True, blank=True)
    commandinstance = models.ForeignKey('CommandInstance')

    def get_local_file_url(self, request=None):
        # path = '/api/file/?s=%s' % self.uuid
        # return build_absolute_uri(path, request)
        return self.file_url

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
        AWS_SECRET_ACCESS_KEY = open(os.path.join(settings.BASE_DIR,'key.txt'),
                                     'r').read()
        policy_document = open(os.path.join(settings.BASE_DIR,
                                            'client/policy_document.json'),
                               'r').read()
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
    upload_file = models.URLField(default=False)


class Permission(TimeStampedModel):
    developer = models.ForeignKey(Developer)
    client = models.ForeignKey(ClientUser)
    command = models.ForeignKey(Command)
