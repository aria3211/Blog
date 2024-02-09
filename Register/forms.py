from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=10,widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confrim password",widget=forms.PasswordInput())
    # Customize Validations
    def clean_email(self):
        cd = self.cleaned_data['email']
        if "@gmail" in cd:
            user = User.objects.filter(email=cd).exists()
            if user:
                raise ValidationError("Email is already exists")
            return cd
        raise ValidationError("you Email must be gmail")
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("Username is already exists")
        return username
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')
        if (p1 and p2 ) and p1!= p2:
            raise ValidationError("Password must be same")

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
