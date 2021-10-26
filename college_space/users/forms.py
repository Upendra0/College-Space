from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import admin
from django.contrib.auth import authenticate


class UserCreationForm(UserCreationForm):

    """
    A django model form to create a user. 
    Fields inherited from user model are:
    email - for user's email address,
    first_name, last_name - for user's name,
    profile_pic - for user's picture.

    Additonaly has 2 more fields:
    password1 - To take password,
    password2 - To verify the password.
    """

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form_input form-control', 'id': 'password1_input', 'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form_input form-control', 'id': 'password2_input', 'placeholder': 'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_pic']
        widgets = {
            'email':forms.EmailInput(attrs={'class': 'form_input form-control', 'id': 'email_input', 'placeholder': 'Enter email'}),
            'first_name': forms.TextInput(attrs={'id':'first_name', 'class':'form_input form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'id':'last_name', 'class':'form_input form-control', 'placeholder': 'Last Name'}),
            'profile_pic': forms.FileInput(attrs={'id': 'profile_pic_input', 'class':'form-input form-control'}),
        }

    def save(self, commit=True):
        """
        Create and save the user from form-input into user table.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_password2(self):

        """
        Check that the two password entries match and return the password.
        If passwords don't match, raises a form validation error.
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserChangeForm(forms.ModelForm):

    """
    Django model form to change user. 
    Fields are -
    first_name, last_name - to change user's name,
    department - to change user's department,
    semester - to change user's semester.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'department', 'semester', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'id':'first_name', 'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'id':'last_name', 'class':'form-control'}),
            'department': forms.Select(attrs={'id':'department', 'class':'form-select'}),
            'semester': forms.TextInput(attrs={'id':'semester', 'class':'form-control'}),
            'profile_pic': forms.FileInput(attrs={'id': 'profile_pic', 'class':'form-file'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password',
            'id': 'password',
        }
    ))
    
    link = "/user/verify_account"
    anchor_tag = f'<a href="{link}" class="alert-link"> Click Here </a>'
    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. Note that both "
            "fields is case-sensitive."
        ),
        'inactive': (f'This account is inactive.{anchor_tag} to activate'),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, email=username, password=password)
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
            raise ValidationError(
                " This account is already activated. Please Login")
    except User.DoesNotExist:
        raise ValidationError("No account exist with this email!")


class VeifyEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                             'class': 'form-control', 'id': 'email', 'placeholder': 'Enter email to verify'}), validators=[validate_email])
    otp = forms.IntegerField(widget=forms.TextInput(attrs={
                             'class': 'form-control', 'id': 'otp', 'placeholder': 'Enter 6 digit otp'}), required=False)
