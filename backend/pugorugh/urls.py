from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegisterView
from . import views


app_name = 'pugorugh'
# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^api/user/preferences/$', views.UserPrefView.as_view(), name='preferences-user'),
    url(r'^api/dog/$', views.DogViewSet.as_view(), name='dog-list'),
    url(r'^api/dog/(?P<pk>\d+)/$', views.DogDetailView.as_view(), name='dog-detail'),
    url(r'^api/dog/(?P<pk>\d+)/(?P<status>undecided|liked|disliked)/$',
        views.UserDogStatusUpdateView.as_view(),
        name='status'),
    url(r'^api/dog/(?P<pk>\d+)/(?P<status>undecided|liked|disliked)/next/$',
        views.NextDogView.as_view(),
        name='nextdog'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
])
