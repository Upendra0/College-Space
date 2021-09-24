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
    syllabus_link= Syllabus.get_syllabus_link(department=department, semester=semester)
    subjects= Subject.get_subjects_list(department=department, semester=semester)
    context= {'syllabus_link':syllabus_link, 'subjects':subjects}
    return render(request=request, template_name='resources/study_materials.html', context=context)