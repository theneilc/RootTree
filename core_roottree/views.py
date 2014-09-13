from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from core_roottree.models import *
from core_roottree.serializers import *
from rest_framework.decorators import link, action
from core_roottree.mixins import UUIDLookupViewSetMixin
from traceback import print_exc
from django.utils.datastructures import MultiValueDictKeyError


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
    list_serializer_class = SessionListSerializer
    complete_serializer_class = SessionSerializer
    create_serializer_class = SessionWriteSerializer

    def list(self, request):
        # client long poll
        sessions = self.get_queryset()
        client_uuid = request.QUERY_PARAMS.get('client_uuid')
        if not client_uuid:
            return Response([])
        client = ClientUser.objects.get(uuid=client_uuid)
        # fetch 'Not requested' sessions for client
        # filter on if reverse relationships are not null

        sessions_tasks = sessions.filter(client=client, status='N', commandinstance__command_task__isnull=False)
        sessions_services = sessions.filter(client=client, status='N', commandinstance__command_service__isnull=False)
        sessions_tasks_serialized = self.list_serializer_class(session_tasks).data
        sessions_services_serialized = self.list_serializer_class(session_services).data
        return Response(sessions_tasks_serialized + sessions_services_serialized)

    def retrieve(self, request, pk=None):
        # dev long poll alice
        return super(SessionViewSet, self).retrieve(request)

    def create(self, request):
        # dev execute alice
        try:
            command_id = request.DATA['command']
            args = request.DATA.get('args', '')
            kwargs = request.DATA.get('kwargs', '')
            commandinstance = CommandInstance.objects.create(
                command_id=command_id,
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
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, MultiValueDictKeyError) as e:
            print_exc()
            return Response("Missing key %s." % e.message,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            print_exc()
            return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action()
    def complete(self, request, **kwargs):
        # client task complete
        session = self.get_object()
        session.status = 'C'
        session.save()
        return Response(self.complete_serializer_class(session).data)
