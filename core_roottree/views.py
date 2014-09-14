from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from core_roottree.models import *
from core_roottree.serializers import *
from rest_framework.decorators import link, action
from core_roottree.mixins import UUIDLookupViewSetMixin
from core_roottree.forms import *
from traceback import print_exc
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
import requests


def index(request):
    return HttpResponse("Hello, world. This is roottree")

class ClientUserCreateView(CreateView):
    form_class = ClientUserSignUpForm
    template_name = 'registration/create_clientuser_form.html'
    success_url = '/accounts/success/'

class DevCreateView(CreateView):
    form_class = DevSignUpForm
    template_name = 'registration/create_dev_form.html'
    success_url = '/accounts/success/'

# for accessing S3 files through our server
# abandoned because we're just using public URLs for now
class FileView(views.APIView):
    def get(self, request):
        # check permissions
        session_id = request.QUERY_PARAMS.get('s')
        if not session_id:
            return Response("Missing key 's'",
                            status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.get(uuid=session_id)
        if not session.file_url:
            return Response("No file for this session",
                            status=status.HTTP_404_NOT_FOUND)
        r = requests.get(session.file_url)
        headers = {
            'content-length':r.headers['content-length']
        }
        response = Response(r.content, status=r.status_code,
                            headers=headers,
                            content_type=r.headers['content-type'])
        return response


# for site (getting and setting info)
class ClientUserViewSet(UUIDLookupViewSetMixin, viewsets.ModelViewSet):
    model = ClientUser


# for site (getting and setting info)
class DeveloperViewSet(UUIDLookupViewSetMixin, viewsets.ModelViewSet):
    model = Developer


# for client long poll to get sessions
# get task url on diagram
class SessionViewSet(UUIDLookupViewSetMixin, viewsets.ModelViewSet):
    model = Session
    list_serializer_class = SessionListSerializer
    complete_serializer_class = SessionSerializer
    create_serializer_class = SessionWriteSerializer

    def options(self, request, *args, **kwargs):
        response = super(SessionViewSet, self).options(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    def list(self, request):
        # client long poll
        sessions = self.get_queryset()
        clientuser_user = request.user
        if not clientuser_user:
            return Response([])
        client = ClientUser.objects.get(user=clientuser_user)
        # fetch 'Not requested' sessions for client
        # filter on if reverse relationships are not null

        sessions_tasks = sessions.filter(client=client, status='P', commandinstance__command_task__isnull=False)
        sessions_services = sessions.filter(client=client, status='P', commandinstance__command_service__isnull=False)
        sessions_tasks_serialized = self.list_serializer_class(sessions_tasks, many=True).data
        sessions_services_serialized = self.list_serializer_class(sessions_services, many=True).data

        return Response(sessions_tasks_serialized + sessions_services_serialized)

    def retrieve(self, request, **kwargs):
        # dev long poll alice
        session = self.get_object()
        if session.status == 'C':
            return Response(session.get_result())
        else:
            return Response()

    def create(self, request):
        # dev execute alice
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Max-Age": "1000",
            "Access-Control-Allow-Headers": "*"
        }
        try:
            command_name = request.DATA['command']
            args = request.DATA.get('args', '')
            kwargs = request.DATA.get('kwargs', '')
            command = Command.objects.get(name=command_name)
            commandinstance = CommandInstance.objects.create(
                command=command,
                args=args,
                kwargs=kwargs
            )
            data = request.DATA.copy()
            data['commandinstance'] = commandinstance.id
            serializer = self.create_serializer_class(data=data)
            if serializer.is_valid():
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                success_headers = self.get_success_headers(serializer.data)
                # really really open access control settings to start
                headers = headers.update(success_headers)
                return Response(self.object.uuid, status=status.HTTP_201_CREATED,
                                headers=headers)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,
                            headers=headers)
        except (KeyError, MultiValueDictKeyError) as e:
            print_exc()
            return Response("Missing key %s." % e.message,
                            status=status.HTTP_400_BAD_REQUEST,
                            headers=headers)
        except:
            print_exc()
            return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            headers=headers)

    @action()
    def complete(self, request, **kwargs):
        # client task complete
        session = self.get_object()
        result_url = request.DATA.get('s3_url')
        session.result_url = result_url
        session.status = 'C'
        session.save()
        return Response(self.complete_serializer_class(session).data)
