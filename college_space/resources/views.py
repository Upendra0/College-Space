from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Note, Subject, Taught,Book, Syllabus, WebTutorial, VideoTutorial, QuestionPaper
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
    dept_name = request.user.department
    semester = request.user.semester
    if dept_name is None:
        dept_name = request.session.get('department', None)
    if semester is None:
        semester = request.session.get('semester', None)
    if request.method=='GET' and (dept_name is None or semester is None):
        next_url = 'subjects'
        return redirect(to='get_department_semester', next_url=next_url)   
    elif request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
        request.session['department'] = dept_name
        request.session['semester'] = semester
    form_data = {'dept_name':dept_name, 'semester':semester}
    form = DepartmentSemesterForm(data=form_data)
    subjects = Taught.get_subjects(dept_name= dept_name, semester=semester)
    context= {'subjects': subjects, 'breadcrumbs':breadcrumbs, 'form':form}
    return render(request=request, template_name='resources/subjects.html', context=context)

@login_required
def syllabus(request):
    breadcrumbs = {'Home':reverse('home'), 'Syllabus':'None'}
    dept_name = request.user.department
    semester = request.user.semester
    if dept_name is None:
        dept_name = request.session.get('department', None)
    if semester is None:
        semester = request.session.get('semester', None)
    if request.method=='GET' and (dept_name is None or semester is None):
        next_url = 'syllabus'
        return redirect(to='get_department_semester', next_url=next_url)  
    elif request.method=='POST':
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
        request.session['department'] = dept_name
        request.session['semester'] = semester

    form_data = {'dept_name':dept_name, 'semester':semester}
    form = DepartmentSemesterForm(data=form_data)
    link = Syllabus.get_view_link(dept_name=dept_name, semester=semester)
    view_link = None
    if link:
        view_link = link[0]['view_link']
    context = {'view_link': view_link, 'breadcrumbs':breadcrumbs, 'form':form}
    return render(request, template_name='resources/syllabus.html', context=context)

@login_required
def online_tutorials(request, sub_code):
    sub_name = Subject.get_name(sub_code=sub_code)
    context = {}
    error_message = None
    if sub_name is None:
        sub_name = ""
        error_message = "This subject does not exist."
    else:
        video_tutorials = VideoTutorial.get_videos(sub_code=sub_code)
        web_tutorials = WebTutorial.get_web_tutorials(sub_code=sub_code)
        sub_name = "-" + sub_name
        if (not video_tutorials) and (not web_tutorials):
            error_message = "Tutorials are not available now, but will be uploaded soon."
        else:
            context['videos'] = video_tutorials
            context['web_tutorials'] = web_tutorials
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), f'Online Tutorials {sub_name}':'None'}
    context['error'] = error_message
    context['breadcrumbs'] = breadcrumbs
    return render(request=request, template_name='resources/online_tutorials.html', context=context)

@login_required
def books(request, sub_code):
    sub_name = Subject.get_name(sub_code=sub_code)
    context = {}
    error_message = None
    if sub_name is None:
        sub_name = ""
        error_message = "This subject does not exist."
    else:
        books = Book.get_books(sub_code=sub_code) 
        sub_name = "-"+sub_name
        if not books:
            error_message = "Books are not available now, but will be uploaded soon."  
        else:
            context['books'] = books 
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), f'Books{sub_name}':'None'}
    context['error'] = error_message
    context['breadcrumbs'] = breadcrumbs
    return render(request=request, template_name='resources/books.html', context=context)


@login_required
def notes(request, sub_code):
    sub_name = Subject.get_name(sub_code=sub_code)
    context = {}
    error_message = None
    if sub_name is None:
        sub_name = ""
        error_message = "This subject does not exist."
    else:
        notes = Note.get_all_notes(sub_code=sub_code)
        sub_name = "-"+sub_name
        if not notes:
            error_message = "Notes are not available now, but will be uploaded soon."  
        else:
            context['notes'] = notes 
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), f'Books{sub_name}':'None'}
    context['error'] = error_message
    context['breadcrumbs'] = breadcrumbs
    return render(request=request, template_name='resources/notes.html', context=context)

@login_required
def question_papers(request, sub_code):
    sub_name = Subject.get_name(sub_code=sub_code)
    context = {}
    error_message = None
    if sub_name is None:
        sub_name = ""
        error_message = "This subject does not exist."
    else:
        question_papers = QuestionPaper.get_question_papers(sub_code=sub_code)
        sub_name = "-"+sub_name
        if not question_papers:
            error_message = "Question papers are not available now, but will be uploaded soon."  
        else:
            context['question_papers'] = question_papers
    breadcrumbs = {'Home':reverse('home'), 'Subject':reverse('subjects'), f'Books{sub_name}':'None'}
    context['error'] = error_message
    context['breadcrumbs'] = breadcrumbs
    return render(request=request, template_name='resources/question_papers.html', context=context)

@login_required
def get_department_semester(request, next_url):
    next_url = reverse(next_url)
    form = DepartmentSemesterForm()
    context = {'form':form, 'next_url': next_url}
    return render(request=request, template_name='resources/department_semester_form.html', context=context)


def team(request):
    return render(request, template_name="resources/team.html")