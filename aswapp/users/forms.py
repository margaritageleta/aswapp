from django import forms

class ProfileForm(forms.Form): 
    username = forms.CharField(max_length=80)
    description = forms.CharField(max_length=500)