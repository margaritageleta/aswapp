from django import forms


class SubmissionForm(forms.Form): 
    title = forms.CharField(required=True)
    url = forms.URLField()
    text = forms.CharField()


