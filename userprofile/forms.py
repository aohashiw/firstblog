from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 =forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = ('username','email')
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 2:
            raise forms.ValidationError("Your username must be at least 2 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_result = User.objects.filter(email__exact=email)
        if len(filter_result) > 0:
            raise forms.ValidationError("Your email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password) > 20:
            raise forms.ValidationError("Your password is too long.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")
        return password2



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','icon','bio')
