from rest_framework import serializers
from core_roottree.models import *

class SessionWriteSerializer(serializers.ModelSerializer):
    developer = serializers.PrimaryKeyRelatedField()
    client = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Session
        fields = ('command', 'args', 'kwargs', 'developer', 'client')
