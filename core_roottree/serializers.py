from rest_framework import serializers
from core_roottree.models import *


class SessionWriteSerializer(serializers.ModelSerializer):
    developer = serializers.SlugRelatedField(slug_field='uuid')
    client = serializers.SlugRelatedField(slug_field='uuid')
    commandinstance = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Session
        fields = ('commandinstance', 'developer', 'client')


class SessionListSerializer(serializers.ModelSerializer):
	code = serializers.Field(source='commandinstance.command.code')
	language = serializers.Field(source='commandinstance.command.language')
	s3_signature = serializers.Field(source='s3_signature')
	stdin = serializers.Field(source='commandinstance.stdin')
	upload_file = serializers.Field(source='commandinstance.command.upload_file')
	args = serializers.Field(source='commandinstance.args')

	# def get_code_with_args(self, obj)
	# 	if obj.commandinstance.args:
			
	# 		code = serializers.Field(source='commandinstance.command.code')

	class Meta:
		model = Session
		fields = ('code', 'language', 'uuid', 's3_signature', 'stdin', 'upload_file')


class SessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Session
		fiels = ('uuid', 'client', 'developer', 'status', 'result', 'callback_url', 'commandinstance')
