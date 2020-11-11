from django import forms


class SubmissionForm(forms.Form): 
    title = forms.CharField(required=True, label="title")
    url = forms.URLField(required=False, label="url")
    text = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=160,
        label="text"
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ), 
        max_length=160,
        label=''
    )