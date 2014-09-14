from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from django.views.generic import TemplateView
from core_roottree import views
from django.contrib.auth.views import login, logout
from django.views.decorators.clickjacking import xframe_options_exempt

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'developers', views.DeveloperViewSet)
router.register(r'clients', views.ClientUserViewSet)
router.register(r'commands', views.CommandViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'roottree.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', xframe_options_exempt(TemplateView.as_view(template_name='index.html')),
        name='home'),
    url(r'^test/$', 'core_roottree.views.index'),
    url(r'^api/', include(router.urls)),
    # url(r'^api/file/', views.FileView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/clientuser/$',  xframe_options_exempt(login), {'template_name':'registration/clientuser_login.html'}),
    url(r'^accounts/login/clientuser/cross_domain/$',  xframe_options_exempt(login), {'template_name':'registration/clientuser_login_cross_domain.html'}),
    url(r'^accounts/login/dev/$',  xframe_options_exempt(login), {'template_name':'registration/dev_login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/delete_cookie/$', views.DeleteCookieView.as_view()),
    url(r'^accounts/register/dev/$', views.DevCreateView.as_view()),
    url(r'^accounts/register/clientuser/$', views.ClientUserCreateView.as_view()),
    url(r'^accounts/set_cookie/$', xframe_options_exempt(views.SetCookieView.as_view())),
    url(r'^accounts/set_cookie/cross_domain/$', xframe_options_exempt(views.SetCookieViewDomain.as_view())),
    url(r'^accounts/success/$', xframe_options_exempt(views.SignUpSuccessView.as_view()))
)
