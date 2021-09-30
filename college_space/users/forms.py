from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form_input form-control', 'id': 'email_input','placeholder':'Enter email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form_input form-control', 'id': 'name_input','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form_input form-control', 'id': 'name_input','placeholder':'Last Name'})
        self.fields['department'].widget.attrs.update({'class': 'form_input form-control', 'id': 'department_input'})
        self.fields['semester'].widget.attrs.update({'class': 'form_input form-control', 'id': 'semester_input', 'min':1, 'max':8 ,'placeholder':'Semester'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form_input form-control', 'id': 'profile_pic_input'})

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class':'form_input form-control', 'id':'password1_input','placeholder':'Password'}), required=True)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form_input form-control', 'id':'password2_input','placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name',
                  'department', 'semester', 'profile_pic']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'department', 'semester', 'profile_pic']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control login-inpu', 'placeholder': '', 'id': 'email_input'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control login-inpu','placeholder': '', 'id': 'password_input',
        }
))
