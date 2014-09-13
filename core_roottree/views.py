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
    list_serializer_class = SessionListSerializer
    complete_serializer_class = SessionSerializer

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
        self.serializer_class = SessionWriteSerializer
        return super(SessionViewSet, self).create(request)

    @action()
    def complete(self, request, **kwargs):
        # client task complete
        session = self.get_object()
        session.status = 'C'
        session.save()
        return Response(self.complete_serializer_class(session).data)
