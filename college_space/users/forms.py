from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import admin
from django.contrib.auth import authenticate


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form_input form-control', 'id': 'email_input','placeholder':'Enter email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form_input form-control', 'id': 'name_input','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form_input form-control', 'id': 'name_input','placeholder':'Last Name'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form_input form-control', 'id': 'profile_pic_input'})

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class':'form_input form-control', 'id':'password1_input','placeholder':'Password'}), required=True)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form_input form-control', 'id':'password2_input','placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_pic']

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

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'department', 'semester', 'profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'id':'myfile', 'style': 'display:None'})
        }

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
        ))

    inactive_link = "<a href=" + "'"+ "http://127.0.0.1:8000/user/verify_account/" +"'" +"class='alert-link'> Click Here </a>"
    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. Note that both "
            "fields is case-sensitive."
        ),
        'inactive': ("This account is inactive."+inactive_link),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, email=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except:
                    user_temp = None

                if user_temp is not None and user_temp.check_password(password):
                        self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data



class GroupAdminForm(forms.ModelForm):
    """
    ModelForm that adds an additional multiple select field for managing
    the users in the group.
    """
    users = forms.ModelMultipleChoiceField(
        User.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Users', False),
        required=False,
        )


    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list('pk', flat=True)
            self.initial['users'] = initial_users


    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)


    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data['users'])


def validate_email(email):
    try:
        user = User.objects.get(email=email)
        if user.is_active:
            raise ValidationError(" This account is already activated. Please Login")
    except User.DoesNotExist:
        raise ValidationError("No account exist with this email!")
    



class VeifyEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'email', 'placeholder':'Enter email to verify'}), validators=[validate_email])
    otp = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'otp', 'placeholder':'Enter 6 digit otp'}), required=False)

    
