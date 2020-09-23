from django import forms
from .models import Image

class IamgeForm(forms.Form):
    title = forms.CharField(max_length=255, label='Title: ')
    picture = forms.ImageField(label='Upload Your Work Here: ')
    submission = forms.ModelChoiceField(empty_label=None, widget=forms.HiddenInput())
    submitter = forms.ModelChoiceField(empty_label=None, widget=forms.HiddenInput())