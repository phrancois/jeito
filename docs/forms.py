from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML


class DocumentSearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u"Chercher..."}))
