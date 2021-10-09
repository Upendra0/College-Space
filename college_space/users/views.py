from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from django.contrib import messages

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
    return render(request=request, template_name='users/profile.html',context={'breadcrumbs':breadcrumbs})
