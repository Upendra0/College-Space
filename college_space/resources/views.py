from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Note, Subject, Taught, Book, Syllabus, WebTutorial, VideoTutorial, QuestionPaper
from .forms import BookForm, DepartmentSemesterForm, NoteForm, QuestionPaperForm, VideoTutorialForm, WebTutorialForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class HomeView(TemplateView):
    
    http_method_names = ['get']

    def get(self, request, **kwargs):
        template_name = 'resources/home.html'
        if request.user.is_authenticated:
            template_name = 'resources/dashboard.html'
        return render(request=request, template_name=template_name)


class SyllabusView(LoginRequiredMixin, TemplateView):
    template_name = 'resources/syllabus.html'

    def get(self, request, *args, **kwargs):
        dept_name = request.user.get_department(request)
        semester = request.user.get_semester(request)
        if dept_name is None or semester is None:
            msg = "Please Update your profile to include department and semester."
            messages.warning(request, msg)
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
        request.session['dept_name'] = dept_name
        request.session['semester'] = semester
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, dept_name, semester, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        breadcrumbs = {'Home': reverse('home'), 'Syllabus': 'None'}
        form_data = {'dept_name': dept_name, 'semester': semester}
        form = DepartmentSemesterForm(data=form_data)
        link = Syllabus.get_view_link(dept_name=dept_name, semester=semester)
        view_link = None
        if link:
            view_link = link[0]['view_link']
        context['view_link'] = view_link
        context['breadcrumbs'] = breadcrumbs
        context['form'] = form
        return context


class ResourceListView(LoginRequiredMixin, TemplateView):

    template_name = "resources/resources.html"

    def get_view_context(self, **kwargs):
        views = ['notes', 'books', 'online_tutorials', 'question_papers']
        views_list = []
        for view in views:
            views_list.append({'view_name':view, 'view_url':reverse(view)})
        return views_list

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context['views'] = self.get_view_context()
        return context

class SubjectView(LoginRequiredMixin, TemplateView):
    template_name = "resources/subjects.html"

    def get(self, request, *args, **kwargs):
        dept_name = request.user.get_department(request)
        semester = request.user.get_semester(request)
        if dept_name is None or semester is None:
            msg = "Please Update your profile to include department and semester."
            messages.warning(request, msg)
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')
        request.session['dept_name'] = dept_name
        request.session['semester'] = semester
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, dept_name, semester, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        form_data = {'dept_name': dept_name, 'semester': semester}
        form = DepartmentSemesterForm(data=form_data)
        subjects = Taught.get_subjects(dept_name= dept_name, semester=semester)
        next_url = self.kwargs.get('next_url')
        breadcrumbs = {'Home': reverse('home'), next_url: 'None'}
        context['subjects'] = subjects
        context['form'] = form
        context['next_url'] = next_url
        context['breadcrumbs'] = breadcrumbs
        return context


class ResourceAbstractView(LoginRequiredMixin, TemplateView):

    def get(self, request, **kwargs):
        sub_code = self.kwargs.get('sub_code', None)
        context = self.get_context_data(**kwargs)
        if sub_code is None:
            return redirect(to='subjects', next_url = self.url)
        else:
            return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        sub_code = self.kwargs.get('sub_code')
        error_message = None
        if sub_code is None:
            context['next_url'] = self.url 
        else:
            sub_name = Subject.get_name(sub_code=sub_code)
            if sub_name is None:
                sub_name = ""
                error_message = "This subject does not exist."
            else:
                breadcrumbs = {'Home': reverse('home'),self.url:reverse(self.url) ,f'{sub_name}':'None'}
                context['breadcrumbs'] = breadcrumbs
        context['error'] = error_message
        return context


class OnlineTutorialView(ResourceAbstractView):

    template_name = "resources/online_tutorials.html"
    url = "online_tutorials"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        sub_code = self.kwargs.get('sub_code')
        if not context['error']:
            video_tutorials = VideoTutorial.get_videos(sub_code=sub_code)
            web_tutorials = WebTutorial.get_web_tutorials(sub_code=sub_code)
            if (not video_tutorials) and (not web_tutorials):
                error_message = "Tutorials are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['videos'] = video_tutorials
                context['web_tutorials'] = web_tutorials
        return context


class BookView(ResourceAbstractView):

    template_name = "resources/books.html"
    url = "books"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        sub_code = self.kwargs.get('sub_code')
        if not context['error']:
            books = Book.get_books(sub_code=sub_code)
            if not books:
                error_message = "Books are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['books'] = books
        return context


class NoteView(ResourceAbstractView):
    template_name = "resources/notes.html"
    url = 'notes'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        sub_code = self.kwargs.get('sub_code')
        if not context['error']:
            notes = Note.get_all_notes(sub_code=sub_code)
            if not notes:
                error_message = "Notes are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['notes'] = notes
        return context


class QuestionPaperView(ResourceAbstractView):

    template_name = "resources/question_papers.html"
    url = "question_papers"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(heading="Question Papers", **kwargs)
        sub_code = self.kwargs.get('sub_code')
        if not context['error']:
            question_papers = QuestionPaper.get_question_papers(
                sub_code=sub_code)
            if not question_papers:
                error_message = "Question Papers are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['question_papers'] = question_papers
        return context

class ContributeView(ResourceListView):
    
    def get_view_context(self, **kwargs):
        views = ['contribute-notes', 'contribute-question_papers', 'contribute-books', 'contribute-video_tutorials', 'contribute-web_tutrials']
        view_name = ['Note', 'Question Paper', 'Book', 'VideoTutorial', 'WebTutorial']
        views_list = []
        for i in range(len(views)):
            views_list.append({'view_name':view_name[i], 'view_url':reverse('subjects',kwargs= {'next_url':views[i]})})
        return views_list

class ContributeFormView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.contributor = self.request.user
        msg = "Your request is submitted succesfully. After a succesfull review by our team, this will be uploaded. Thanks!"
        messages.success(self.request, msg)
        return super().form_valid(form)


class ContributeNoteView(ContributeFormView):
    model = Note
    form_class = NoteForm
    template_name = "resources/contribute_notes.html"
    success_url = reverse_lazy('contribute')


class ContributeQuestionPaperView(ContributeFormView):
    model = QuestionPaper
    form_class = QuestionPaperForm
    template_name = "resources/contribute_question_paper.html"
    success_url = reverse_lazy('contribute')


class ContributeBookView(ContributeFormView):
    model = Book
    form_class = BookForm
    template_name = "resources/contribute_books.html"
    success_url = reverse_lazy('contribute')


class ContributeVideoTutorialView(ContributeFormView):
    model = VideoTutorial
    form_class = VideoTutorialForm
    template_name = "resources/contribute_video_tutorials.html"
    success_url = reverse_lazy('contribute')


class ContributeWebTutorialView(ContributeFormView):
    model = WebTutorial
    form_class = WebTutorialForm
    template_name = "resources/contribute_web_tutorials.html"
    success_url = reverse_lazy('contribute')


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = "resources/team.html"
