from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views as core_views

app_name = 'core'

urlpatterns = [
    url(r'^$', core_views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
]
