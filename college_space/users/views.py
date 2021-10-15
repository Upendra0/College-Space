from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .models import User
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect(to='home')
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.info(request, "Please Verify your account.")
            return redirect(to='verify_account_with_email', email=user.email)
        else:
            return render(request=request, template_name='users/register.html', context={'form':form})
    form = forms.UserCreationForm()
    return render(request=request, template_name='users/register.html', context={'form':form})

class MyLoginView(LoginView):
    template_name='users/login.html'
    redirect_authenticated_user=True
    authentication_form = forms.UserLoginForm

@login_required
def profile(request):
    breadcrumbs = {'Home':reverse('home'),  'Profile':'None'}
    form = None
    if request.method == 'POST':
        form = forms.UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        first_name = request.user.first_name
        last_name = request.user.last_name
        department = request.user.department
        semester = request.user.semester
        user_data = {'first_name':first_name, 'last_name':last_name, 'department':department, 'semester':semester}
        form = forms.UserChangeForm(user_data)
    return render(request=request, template_name='users/profile.html',context={'form':form, 'breadcrumbs':breadcrumbs})

def send_otp(request, email, template):
    form = None
    if email:
        form = forms.VeifyEmailForm(data={'email':email})
        if form.is_valid():
            user = User.objects.get(email=email)
            user.send_otp()
            msg = "A 6 digit Otp has been sent to your mail. Please check Inbox"
            messages.success(request, message=msg)
    else:
        form = forms.VeifyEmailForm()
    return render(request, template_name=template, context={'form':form})

def verify_account(request, email=None):
    template_name = "users/verify_account.html"
    if request.method=='GET':
        return send_otp(request, email, template=template_name)
    else:
        form = forms.VeifyEmailForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            action = request.POST.get('action')
            if action=='send':
                return send_otp(request, email, template_name)
            else:
                otp = request.POST.get('otp')
                user = User.objects.get(email=email)
                if user.verify_otp(otp):
                    user.is_active = True
                    user.save()
                    login(request, user)
                    msg = "Your account is activated."
                    messages.success(request, msg)
                    return redirect(to='home')
                else:
                    form.add_error(field=None, error='OTP Does not match')
        return render(request,template_name=template_name, context={'form':form})

