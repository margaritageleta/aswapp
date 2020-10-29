from django import forms


class SubmissionForm(forms.Form): 
    title = forms.CharField(required=True)
    url = forms.URLField(required=False)
    text = forms.CharField(required=False)


