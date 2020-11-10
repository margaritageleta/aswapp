from django import forms


class SubmissionForm(forms.Form): 
    title = forms.CharField(required=True)
    url = forms.URLField(required=False)
    text = forms.CharField(required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}), max_length=160)