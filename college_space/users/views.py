from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
import pyotp

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(to='home')
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            succes_massage = "Your accout was created succesfully"
            messages.success(request, succes_massage)
            return redirect(to='home')
        else:
            return render(request=request, template_name='users/register.html', context={'form':form})
    form = forms.UserCreationForm()
    return render(request=request, template_name='users/register.html', context={'form':form})

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

@login_required
def verify_account(request):
    secret_key = pyotp.random_base32()
    minute = 10
    otp = pyotp.TOTP(secret_key, interval= int(minute*60))
    subject = "OTP for account confirmation"
    msg = "Hii " + request.user.email + " your otp for email verification is" + otp.now()
    send_mail(subject=subject, message=msg, from_email=None, recipient_list=[request.user.email])
    return redirect(to='home')