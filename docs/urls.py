from django.conf.urls import url
from tagulous.views import autocomplete
from .models import DocumentTags
from . import views as docs_views

app_name = 'docs'

urlpatterns = [
    url(r'^$', docs_views.IndexView.as_view(), name='index'),
    url(r'^create/$', docs_views.DocumentCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', docs_views.DocumentUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', docs_views.DocumentDeleteView.as_view(), name='delete'),
    url(r'^tags_autocomplete/$', autocomplete, {'tag_model': DocumentTags}, name='tags_autocomplete'),
]
