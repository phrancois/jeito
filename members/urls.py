from django.conf.urls import url
from . import views


app_name = 'members'

urlpatterns = [
    url(r'^adhesions/$', views.AdhesionsView.as_view(), name='adhesions'),
    url(r'^adhesions/data/$', views.AdhesionsJsonView.as_view(), name='adhesions_data'),
]
