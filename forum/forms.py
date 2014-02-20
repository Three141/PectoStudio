from django import forms


class NewPostForm(forms.Form):
    title = forms.CharField(max_length=50)
    data = forms.CharField()


class NewCommentForm(forms.Form):
    data = forms.CharField()
