from django import forms
from .models import MainProcess, SubProcess

class MainProcessForm(forms.ModelForm):
    class Meta:
        model = MainProcess
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Main Process Name'}),
        }

class SubProcessForm(forms.ModelForm):
    class Meta:
        model = SubProcess
        fields = ['name', 'additional_info']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Sub Process Name'}),
            'additional_info': forms.Textarea(attrs={'placeholder': 'Enter Additional Info'}),
        }
