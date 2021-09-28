from django.shortcuts import redirect, render
from .models import Syllabus, Subject, Resource, Note
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='resources/home.html')
    return redirect(to='login')

@login_required
def subjects(request):
    department = request.user.department
    semester = request.user.semester
    syllabus_link= Syllabus.get_syllabus_link(department=department, semester=semester)
    subjects= Subject.get_subjects_list(department=department, semester=semester)
    breadcrumbs = {'Home':reverse('home'), 'Subject':'None'}
    context= {'syllabus_link':syllabus_link, 'subjects':subjects, 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/subjects.html', context=context)

@login_required
def reading_tutorials(request):
    sub_code = request.GET.get('subject_code')
    if sub_code is None:
        return redirect(to='subjects')
    books = Resource.get_books_list(sub_code)
    web_tutorials = Resource.get_web_list(sub_code)
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Reading_tutorials':'None'}
    context = {'sub_code': sub_code, 'books':books, 'web_tutorials':web_tutorials, 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/reading_tutorials.html', context=context)

@login_required
def video_tutorials(request):
    sub_code = request.GET.get('subject_code')
    if sub_code is None:
        return redirect(to='subjects')
    videos = Resource.get_vidoes_list(sub_code)
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Video tutorials':'None'}
    context = {'sub_code': sub_code, 'videos': videos, 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/videos.html', context=context)


@login_required
def notes(request):
    sub_code = request.GET.get('subject_code')
    if sub_code is None:
        return redirect(to='subjects')
    all_notes = Note.get_notes_list(sub_code)
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Notes':'None'}
    context = {'sub_code':sub_code, 'notes':all_notes, 'breadcrumbs':breadcrumbs}
    return render(request, template_name='resources/notes.html', context=context)