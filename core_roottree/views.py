from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is roottree")

class TaskAPIView(APIView):
	def post(self, request):
		# get task url
		# return ID
		return Response()

class ClientPollAPIView(APIView):
	def get(self, request):
		# return task
		return Response()

class ClientDoneAPIView(APIView):
	def post(self, request):
		# if file upload to s3 (through model method?)
		return Response()
	
	def get(self, request):
		# long polling from library 
		return Response()