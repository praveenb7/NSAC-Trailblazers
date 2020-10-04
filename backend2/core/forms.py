from django import forms
from .models import UserReport


class UserReportForm(forms.ModelForm):
    class Meta:
        model = UserReport
        exclude = ['location']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
