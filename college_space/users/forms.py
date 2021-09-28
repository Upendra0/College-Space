from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from . import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form_input', 'id': 'email_input'})
        self.fields['first_name'].widget.attrs.update({'class': 'form_input', 'id': 'name_input'})
        self.fields['last_name'].widget.attrs.update({'class': 'form_input', 'id': 'name_input'})
        self.fields['department'].widget.attrs.update({'class': 'form_input', 'id': 'department_input'})
        self.fields['semester'].widget.attrs.update({'class': 'form_input', 'id': 'semester_input', 'min':1, 'max':8})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form_input', 'id': 'profile_pic_input'})

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class':'form_input', 'id':'password1_input'}), required=True)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form_input', 'id':'password2_input'}), required=True)

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
        fields = ['email', 'first_name', 'last_name', 'department', 'semester']
