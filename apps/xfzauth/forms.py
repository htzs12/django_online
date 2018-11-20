from django import forms
from apps.forms import FormMixin


class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=10,min_length=6)
    remember = forms.IntegerField(required=False)