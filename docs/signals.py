from django.db import models
from django.dispatch import Signal
from haystack import signals


post_form_save = Signal()
post_form_delete = Signal()


class DocumentSignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        post_form_save.connect(self.handle_save)
        post_form_delete.connect(self.handle_delete)

    def teardown(self):
        post_form_save.disconnect(self.handle_save)
        post_form_delete.disconnect(self.handle_delete)
