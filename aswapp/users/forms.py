from django import forms

class ProfileForm(forms.Form): 
    description = forms.TextField(
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=1000,
        label='description',
    )