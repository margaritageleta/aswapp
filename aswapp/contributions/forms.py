from django import forms


class SubmissionForm(forms.Form): 
    title = forms.CharField(max_length=80, required=True, label="title")
    url = forms.URLField(required=False, label="url")
    text = forms.TextField(
        required=False, 
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=1000,
        label="text"
    )


class CommentForm(forms.Form):
    comment = forms.TextField(
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=1000,
        label=''
    )