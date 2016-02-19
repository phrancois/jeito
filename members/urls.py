from django.conf.urls import url
from . import views


app_name = 'members'

urlpatterns = [
    url(r'^adhesions/$', views.AdhesionsView.as_view(), name='adhesions'),
    url(r'^adhesions/data/(?P<season>\d{4})/(?P<reference>\d{4})/$', views.AdhesionsJsonView.as_view(), name='adhesions_data'),
]
