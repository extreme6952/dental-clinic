from django import forms

from .models import Comment,Profile

from django.contrib.auth.models import User


class EmailShare(forms.Form):

    name = forms.CharField(max_length=250)

    email = forms.EmailField()

    to = forms.EmailField()

    comments = forms.CharField(widget=forms.Textarea,
                               required=True,)
    


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name','email','body']



class SearchForms(forms.Form):

    query = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mr-sm-2'}))



class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput,
                               label='Придумайте пароль')

    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Повторите пароль-',)

    class Meta:

        model = User

        fields = ['first_name','last_name','email','username']

    def clean_password2(self):

        cd = self.cleaned_data

        if cd['password'] != cd['password2']:

            raise forms.ValidationError('Пароли не совпадают')
        
        return cd['password']
    
    def clean_email(self):
        data = self.cleaned_data["email"]

        if User.objects.filter(email=data):

            raise forms.ValidationError('Данный email уже зарегестрирован')

        return data
    

class UserEditForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ['first_name','last_name','email']

    def clean_email(self):
        data = self.cleaned_data["email"]

        qs = User.objects.exclude(id=self.instance.id).filter(email=data)

        if qs.exists():

            raise forms.ValidationError('Данный email уже используется')
        
        return data
    
class ProfileEditForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ['photo','date_of_birthy',]
        

