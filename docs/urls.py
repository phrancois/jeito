from django.conf.urls import url
from . import views as docs_views

app_name = 'docs'

urlpatterns = [
    url(r'^docs/$', docs_views.IndexView.as_view(), name='index'),
    url(r'^docs/create/$', docs_views.DocumentCreateView.as_view(), name='create'),
    url(r'^docs/update/(?P<pk>\d+)/$', docs_views.DocumentUpdateView.as_view(), name='update'),
    url(r'^docs/delete/(?P<pk>\d+)/$', docs_views.DocumentDeleteView.as_view(), name='delete'),
]
