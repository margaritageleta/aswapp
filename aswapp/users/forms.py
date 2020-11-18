from django import forms

class ProfileForm(forms.Form): 
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=500,
        label='description',
    )