from django import forms
from django.contrib.auth.models import User
from app1.models import UserInfo

class UserForm1(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')

class UserInfo(forms.ModelForm):
    class Meta():
        model=UserInfo
        fields=('portfolio_site','profile_pic')