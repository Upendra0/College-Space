from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Note, Taught,Book, Syllabus, WebTutorial, Video, QuestionPaper
from .forms import DepartmentSemesterForm

# Create your views here.
def home(request):
    template_name = 'resources/home.html'
    if request.user.is_authenticated:
        template_name = 'resources/dashboard.html'        
    return render(request=request, template_name= template_name)

@login_required
def subjects(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':'None'}
    dept_name = None
    semester = None
    if request.method=='GET':
        if request.user.department is None or request.user.semester is None:
            next_url = 'subjects'
            return redirect(to='get_department_semester', next_url=next_url) 
        else:
            dept_name = request.user.department.name
            semester = request.user.semester
    else:
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
    form = DepartmentSemesterForm(data={'dept_name':dept_name, 'semester':semester})
    subjects = Taught.get_subjects(dept_name= dept_name, semester=semester)
    context= {'subjects': subjects, 'breadcrumbs':breadcrumbs, 'form':form}
    return render(request=request, template_name='resources/subjects.html', context=context)

@login_required
def syllabus(request):
    breadcrumbs = {'Home':reverse('home'), 'Syllabus':'None'}
    dept_name = None
    semester = None
    if request.method == 'GET':
        if request.user.department is None or request.user.semester is None:
            next_url = 'syllabus'
            return redirect(to='get_department_semester', next_url=next_url)
        else:
            dept_name = request.user.department.name
            semester = request.user.semester
    else:
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
    form = DepartmentSemesterForm(data={'dept_name':dept_name, 'semester':semester})
    view_link = Syllabus.get_view_link(dept_name=dept_name, semester=semester)
    context = {'view_link': view_link, 'breadcrumbs':breadcrumbs, 'form':form}
    return render(request, template_name='resources/syllabus.html', context=context)

@login_required
def reading_tutorials(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject': reverse('subjects'), 'Reading Tutorials': 'None'}
    sub_code = request.GET.get('subject_code', '??')
    books = Book.get_books(sub_code=sub_code)
    web_tutorials = WebTutorial.get_web_tutorials(sub_code=sub_code)
    context = {'books':books, 'web_tutorials': web_tutorials, 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/reading_tutorials.html', context=context)

@login_required
def video_tutorials(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Video tutorials':'None'}
    sub_code = request.GET.get('subject_code', '??')
    video_tutorials = Video.get_videos(sub_code=sub_code)
    context = {'videos': video_tutorials, 'breadcrumbs':breadcrumbs}
    return render(request=request, template_name='resources/videos.html', context=context)


@login_required
def notes(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Notes':'None'}
    sub_code = request.GET.get('subject_code')
    notes = Note.get_all_notes(sub_code=sub_code)
    context = {'notes':notes, 'breadcrumbs':breadcrumbs}
    return render(request, template_name='resources/notes.html', context=context)

@login_required
def question_papers(request):
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), 'Question Papers':'None'}
    sub_code = request.GET.get('subject_code', '??')
    question_papers = QuestionPaper.get_question_papers(sub_code=sub_code)
    context = {'question_papers':question_papers, 'breadcrumbs':breadcrumbs}
    return render(request, template_name='resources/question_papers.html', context=context)

@login_required
def get_department_semester(request, next_url):
    next_url = reverse(next_url)
    form = DepartmentSemesterForm()
    context = {'form':form, 'next_url': next_url}
    return render(request=request, template_name='resources/department_semester_form.html', context=context)
