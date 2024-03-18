from django import forms

from .models import Comment

from django.contrib.auth.models import User


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



class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User

        fields = ['first_name','last_name','email','username']

    def clean_password2(self):

        cd = self.cleaned_data

        if cd['password'] != cd['password2']:

            raise forms.ValidationError('Пароли не совпадают')
        
        return cd['password']

