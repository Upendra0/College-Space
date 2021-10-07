from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def home(request):
    template_name = 'resources/home.html'
    if request.user.is_authenticated:
        template_name = 'resources/dashboard.html'        
    return render(request=request, template_name= template_name)

@login_required
def subjects(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':'None'}
    context= {'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/subjects.html', context=context)

@login_required
def reading_tutorials(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject': reverse('subjects'), 'Reading Tutorials': 'None'}
    context = {'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/reading_tutorials.html', context=context)

@login_required
def video_tutorials(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Video tutorials':'None'}
    context = { 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/videos.html', context=context)


@login_required
def notes(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Notes':'None'}
    context = { 'breadcrumbs':breadcrumbs}
    return render(request, template_name='resources/notes.html', context=context)