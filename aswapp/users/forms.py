from django import forms

class ProfileForm(forms.Form): 
    description = forms.CharField(max_length=500)