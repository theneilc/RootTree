from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

class ClientUser(models.Model):
    uuid = models.CharField(max_length=32)
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User)


class Developer(models.Model):
    # email = models.EmailField(unique=True, max_length=254)
    user = models.OneToOneField(User)


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
    result = models.TextField(null=True, blank=True)
    callback_url = models.URLField(null=True, blank=True)
    commandinstance = models.ForeignKey('CommandInstance')


class Service(TimeStampedModel):
    commandinstance = models.OneToOneField('CommandInstance')
    lastrun = models.DateTimeField()
    frequency = models.IntegerField()  # time to wait in seconds


class Task(TimeStampedModel):
    commandinstance = models.OneToOneField('CommandInstance')


class CommandInstance(models.Model):
    command = models.ForeignKey('Command')
    args = models.TextField()
    kwargs = models.TextField()


class Command(TimeStampedModel):
    code = models.TextField()
    owner = models.ForeignKey(Developer, null=True, blank=True)

    """LANGUAGE_CHOICES = (
    (u'
    language = models.CharField(max_length=1, default='b')
    codeTextField (%s for args, %(kwarg_name))
    ownerforeignkey to Developer
    languageCharField
    file_responseBool
    
    """
