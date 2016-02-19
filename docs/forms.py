from django import forms


class DocumentSearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u"Chercher..."}))
