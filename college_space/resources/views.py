from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request=request, template_name='resources/home.html')

@login_required
def study_materials(request):
    return render(request=request, template_name='resources/study_materials.html')