from django import forms

from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class loginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')