import base64
import hmac, hashlib
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from datetime import datetime


DEFAULT_POLL_TIME = datetime(1901,1,1)


class ClientUser(models.Model):
    uuid = models.CharField(max_length=32)
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User)
    lastpolltime = models.DateTimeField(default=DEFAULT_POLL_TIME)


class Developer(models.Model):
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100)

class Session(TimeStampedModel):
    uuid = models.CharField(max_length=32)
    client = models.ForeignKey(ClientUser)
    developer = models.ForeignKey(Developer)

    STATUS_CHOICES = (
        (u'N', u'Not Requested'),
        (u'P', u'Pending'),
        (u'C', u'Complete'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    
    # s3 urls
    file_url = models.TextField(null=True, blank=True)
    result_url = models.TextField(null=True, blank=True)
    # end s3 urls

    callback_url = models.URLField(null=True, blank=True)

    commandinstance = models.ForeignKey('CommandInstance')

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


class Command(TimeStampedModel):
    code = models.TextField()
    owner = models.ForeignKey(Developer, null=True, blank=True)
    LANGUAGE_CHOICES = (
        (u'b', u'bash'),
        (u'p', u'python'),
    )
    language = models.CharField(max_length=1, default='b')
    expectfile = models.BooleanField(default=False)
