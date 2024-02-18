from django import forms

from .models import Comment


class EmailShare(forms.Form):

    name = forms.CharField(max_length=250)

    email = forms.EmailField()

    to = forms.EmailField()

    comments = forms.CharField(widget=forms.Textarea,
                               required=True)
    


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name','email','body']



class SearchForms(forms.Form):

    query = forms.CharField()