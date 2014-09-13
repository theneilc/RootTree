from rest_framework import serializers
from core_roottree.models import *

class SessionListSerializer(serializers.ModelSerializer):
	code = serializers.Field(source='commandinstance.command.code')
	language = serializers.Field(source='commandinstance.command.language')

	class Meta:
		model = Session
		fields = ('code', 'language', 'uuid', 's3_signature')