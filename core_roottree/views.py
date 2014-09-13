from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from core_roottree.models import *
from core_roottree.serializers import *
from rest_framework.decorators import link, action
from core_roottree.mixins import UUIDLookupViewSetMixin

def index(request):
    return HttpResponse("Hello, world. This is roottree")


# for site (getting and setting info)
class ClientUserViewSet(viewsets.ModelViewSet, UUIDLookupViewSetMixin):
	model = ClientUser


# for site (getting and setting info)
class DeveloperViewSet(viewsets.ModelViewSet, UUIDLookupViewSetMixin):
	model = Developer


# for client long poll to get sessions
# get task url on diagram
class SessionViewSet(viewsets.ModelViewSet, UUIDLookupViewSetMixin):
	model = Session

	def list(self, request):
		# client long poll
		sessions = self.get_queryset()
		return super(SessionViewSet, self).list(request)

	def retrieve(self, request, pk=None):
		# dev long poll alice
		return super(SessionViewSet, self).retrieve(request)

        def create(self, request):
            # dev execute alice
            self.serializer_class = SessionWriteSerializer
            return super(SessionViewSet, self).create(request)

"""
accepts the following from the form dict -- 
'command_id', 'args', 'kwargs' (string representation of dictionary),
'dev_key', 'client_id'. Checks to see if permissions are okay and if the devs
are accessing a function they're allowed to (custom command). Generates 
Session and CommandInstance. Returns session uuid.

URL (POST): /api/sessions/

VIEW FUNCTION: SessionViewSet.create
"""
	@action()
	def complete(self, request, **kwargs):
		# client task complete
		session = Session.objects.get(uuid=kwargs.get('uuid'))
		session.status = 'C'
		session.save()
		return Response()
