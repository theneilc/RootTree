from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from django.views.generic import TemplateView
from core_roottree import views

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'roottree.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'),
        name='home'),
    url(r'^test$', 'core_roottree.views.index'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
