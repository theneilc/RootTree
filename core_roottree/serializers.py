from rest_framework import serializers
from core_roottree.models import *

class SessionListSerializer(serializers.ModelSerializer):
	code = serializers.Field(source='commandinstance.command.code')
	language = serializers.Field(source='commandinstance.command.language')
	s3_signature = serializers.Field(source='s3_signature')
	class Meta:
		model = Session
		fields = ('code', 'language', 'uuid', 's3_signature')

class SessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Session
		fiels = ('uuid', 'client', 'developer', 'status', 'result', 'callback_url', 'commandinstance')