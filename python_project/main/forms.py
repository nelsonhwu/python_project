from django import forms
from .models import Image

class ImageForm(forms.Form):
    title = forms.CharField(max_length=255, label='Title: ')
    picture = forms.ImageField(label='Upload Your Work Here: ')
    submission = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        empty_label=None, 
        widget=forms.HiddenInput()
        )
    submitter = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        empty_label=None, 
        widget=forms.HiddenInput()
        )