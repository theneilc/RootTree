from rest_framework import serializers
from core_roottree.models import *

class SessionWriteSerializer(serializers.ModelSerializer):
    developer = serializers.SlugRelatedField(slug_field='uuid')
    client = serializers.SlugRelatedField(slug_field='uuid')

    class Meta:
        model = Session
        fields = ('command', 'args', 'kwargs', 'developer', 'client')
