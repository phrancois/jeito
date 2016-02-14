from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from . import models as docs_models


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'docs/index.html'
    model = docs_models.Document


class CrispyFormViewMixin(object):
    glyphicon = 'ok-sign'
    submit_text = u"OK"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.layout = Layout(*self.fields)
        form.helper.layout.append(
            HTML(u"""<button type="submit" class=\"btn btn-success\">
                       <span class="glyphicon glyphicon-{glyphicon}"></span> {text}
                     </button>""".format(glyphicon=self.glyphicon, text=self.submit_text))
        )
        form.helper.layout.append(
            HTML(u"""<a href=\"{href}\" class=\"btn btn-default\">
                       <span class="glyphicon glyphicon-remove-sign"></span> Annuler
                     </a>""".format(href=self.success_url))
        )
        return form


class DocumentCreateView(LoginRequiredMixin, CrispyFormViewMixin, CreateView):
    model = docs_models.Document
    fields = ('title', 'file')
    success_url = reverse_lazy('docs:index')
    glyphicon = 'plus'
    submit_text = u"Ajouter"


class DocumentUpdateView(LoginRequiredMixin, CrispyFormViewMixin, UpdateView):
    model = docs_models.Document
    fields = ('title', 'file')
    success_url = reverse_lazy('docs:index')
    submit_text = u"Modifier"


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = docs_models.Document
    success_url = reverse_lazy('docs:index')
