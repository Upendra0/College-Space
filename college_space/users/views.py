from django.shortcuts import redirect, render
from . import forms

# Create your views here.

def register(request):
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='home')
    form = forms.UserCreationForm()
    return render(request=request, template_name='users/register.html', context={'form':form})


def login(request):
    pass

def logout(request):
    pass
