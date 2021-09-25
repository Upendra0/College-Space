from django.shortcuts import redirect, render
from .models import Syllabus, Subject, Resource, Note
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request=request, template_name='resources/home.html')

@login_required
def subjects(request):
    department = request.user.department
    semester = request.user.semester
    syllabus_link= Syllabus.get_syllabus_link(department=department, semester=semester)
    subjects= Subject.get_subjects_list(department=department, semester=semester)
    context= {'syllabus_link':syllabus_link, 'subjects':subjects}
    return render(request=request, template_name='resources/subjects.html', context=context)

@login_required
def study_materials(request):
    sub_code = request.GET.get('subject_code')
    if sub_code is None:
        return redirect(to='subjects')
    resources = Resource.get_resources_list(sub_code)
    context = {'sub_code': sub_code, 'resources':resources}
    return render(request=request, template_name='resources/study_materials.html', context=context)

@login_required
def notes(request):
    sub_code = request.GET.get('subject_code')
    if sub_code is None:
        return redirect(to='subjects')
    all_notes = Note.get_notes_list(sub_code)
    context = {'sub_code':sub_code, 'notes':all_notes}
    return render(request, template_name='resources/notes.html', context=context)