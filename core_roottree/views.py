from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView, ModelViewset
from rest_framework.response import Response
from core_roottree.models import *
from rest_framework.decorators import link, action

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is roottree")

# for site (getting and setting info)
class ClientUserViewSet(viewsets.ModelViewSet):
	model = ClientUser

# for site (getting and setting info)
class DeveloperViewSet(viewsets.ModelViewSet):
	model = Developer

# for client long poll to get sessions
# get task url on diagram
class SessionViewSet(viewsets.ModelViewSet):
	model = Session

	def list(self, request):
		# client long poll
		return Response()

	def retrieve(self, request, pk=None):
		# dev long poll
		return Response()

	def create(self, request):
		# dev execute
		return Response()

	@action()
	def complete(self, request, **kwargs):
		# client task complete
		return Response()
