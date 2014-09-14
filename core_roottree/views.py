from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
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
from django.views.generic import TemplateView
from django.contrib.auth.models import User
import requests


class SignUpSuccessView(TemplateView):
    template_name = 'registration/success.html'

    def get(self, request, *args, **kwargs):
        # response = SimpleTemplateResponse(template=self.template_name)
        # if not request.user.is_anonymous():
        #     if request.user.related_clientuser:
        #         response.set_cookie('clientuser_uuid', request.user.related_clientuser.uuid)
        # return response
        return super(SignUpSuccessView, self).get(request, *args, **kwargs)

class DeleteCookieView(TemplateView):
    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        response = SimpleTemplateResponse(template=self.template_name)
        response.delete_cookie('uuid')
        return response

class SetCookieViewDomain(TemplateView):
    template_name = 'registration/settingcookie.html'

    def get(self, request, *args, **kwargs):
        print "fuck you domain"
        print "request.GET", request.GET
        uuid = request.user.related_clientuser.uuid
        url = '/?uuid='+uuid
        response = HttpResponseRedirect(url)
        if not request.user.is_anonymous():
            if request.user.related_clientuser:
                response.set_cookie('uuid', request.user.related_clientuser.uuid)
                response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

        return response

class SetCookieView(TemplateView):
    template_name = 'registration/settingcookie.html'

    def get(self, request, *args, **kwargs):
        print "fuck you dude"
        print "request.GET", request.GET
        response = HttpResponseRedirect('/')
        if not request.user.is_anonymous():
            if request.user.related_clientuser:
                response.set_cookie('uuid', request.user.related_clientuser.uuid)
                response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

        return response

def index(request):
    return SimpleTemplateResponse(template='js/example.html')

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

class CommandViewSet(UUIDLookupViewSetMixin, viewsets.ModelViewSet):
    model = Command

# for client long poll to get sessions
# get task url on diagram
class SessionViewSet(UUIDLookupViewSetMixin, viewsets.ModelViewSet):
    model = Session
    list_serializer_class = SessionListSerializer
    complete_serializer_class = SessionSerializer
    create_serializer_class = SessionWriteSerializer

    def allow_cross_domain(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-CSRFToken"
        return response

    def get_permissions(self):
        ret = super(SessionViewSet, self).get_permissions()
        print 'permissions', ret
        print 'method', self.request.method
        if self.request.method == 'OPTIONS' or self.request.method == 'POST'\
           or (self.request.method == 'GET' and self.kwargs.get('pk')):
            # temporary. move to authentication.
            return []
        else:
            return ret

    def options(self, request, *args, **kwargs):
        return self.allow_cross_domain(
            super(SessionViewSet, self).options(request, *args, **kwargs)
        )

    def list(self, request):
        # client long poll
        sessions = self.get_queryset()
        clientuser_user = request.user
        if not clientuser_user:
            return Response([])
        client = ClientUser.objects.get(user=clientuser_user)

        # fetch 'Not requested' sessions for client
        sessions_tasks = sessions.filter(client=client, status='N', commandinstance__command_task__isnull=False)
        sessions_services = sessions.filter(client=client, status='N', commandinstance__command_service__isnull=False)
        sessions_tasks_serialized = self.list_serializer_class(sessions_tasks, many=True).data
        sessions_services_serialized = self.list_serializer_class(sessions_services, many=True).data

        # update the sessions to Pending
        sessions_tasks.update(status='P')
        sessions_services.update(status='P')

        return Response(sessions_tasks_serialized + sessions_services_serialized)

    def retrieve(self, request, **kwargs):
        # dev long poll alice
        session = self.get_object()
        if session.status == 'C':
            return self.allow_cross_domain(Response(session.get_result()))
        else:
            return self.allow_cross_domain(Response('pending'))

    def create(self, request):
        # dev execute alice
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
            # todo add in services later
            task = Task.objects.create(
                commandinstance=commandinstance
            )
            data = request.DATA.copy()
            data['commandinstance'] = commandinstance.id
            serializer = self.create_serializer_class(data=data)
            if serializer.is_valid():
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                return self.allow_cross_domain(
                    Response(self.object.uuid, status=status.HTTP_201_CREATED,
                             headers=headers))

            return self.allow_cross_domain(
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

        except (KeyError, MultiValueDictKeyError) as e:
            print_exc()
            return self.allow_cross_domain(
                Response("Missing key %s." % e.message,
                         status=status.HTTP_400_BAD_REQUEST))

        except Command.DoesNotExist as e:
            print_exc()
            return self.allow_cross_domain(
                Response("Command %s does not exist" % request.DATA['command'],
                         status=status.HTTP_404_NOT_FOUND))

        except:
            print_exc()
            return self.allow_cross_domain(
                Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR))

    @action()
    def complete(self, request, **kwargs):
        # client task complete
        session = self.get_object()
        result_url = request.DATA.get('s3_url')
        session.result_url = result_url
        session.status = 'C'
        session.save()
        return Response(self.complete_serializer_class(session).data)

class DevHomeView(TemplateView):
    template_name = 'dev_home.html'
    def get_context_data(self, **kwargs):
        context = {}
        user = self.request.user
        developer = user.related_developer
        context['company'] = developer.company
        context['url'] = developer.url
        context['uuid'] = developer.uuid
        context['commands'] = CommandSerializer(Command.objects.all(), many=True).data
        return context


