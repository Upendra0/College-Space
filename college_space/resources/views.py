from django.shortcuts import render
from .models import Syllabus, Subject, Resource
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request=request, template_name='resources/home.html')

@login_required
def study_materials(request):
    department = request.user.department
    semester = request.user.semester
    syllabus = Syllabus.objects.get(department=department, semester=semester)
    subject_lists= Subject.objects.filter(department=department, semester=semester)

    subjects=[]
    for subject in subject_lists:
        subjects.append({'name':subject.name, 'credit':subject.credit})

    context= {'syllabus_link':syllabus.download_link, 'subjects':subjects}
    return render(request=request, template_name='resources/study_materials.html', context=context)