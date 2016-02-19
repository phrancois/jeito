import haystack
from django.core.management import call_command
from django.test import TestCase, override_settings
from members.tests import LoggedTestMixin


TEST_HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'TIMEOUT': 60 * 10,
        'INDEX_NAME': 'test_index',
    },
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_HAYSTACK_CONNECTIONS)
class HaystackTestCase(TestCase):
    def setUp(self):
        haystack.connections.reload('default')
        super().setUp()

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)


class LoggedTests(LoggedTestMixin, HaystackTestCase):
    def test_index_view(self):
        response = self.client.get('/docs/')
        self.assertContains(response, '<li class="active">Documents</li>')
