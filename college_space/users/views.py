from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(to='home')
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password1'))
            if user is not None:
                login(request, user)
            return redirect(to='home')
        else:
            return render(request=request, template_name='users/register.html', context={'form':form})
    form = forms.UserCreationForm()
    return render(request=request, template_name='users/register.html', context={'form':form})

@login_required
def profile(request):
    return render(request=request, template_name='users/profile.html')
