""" Views for resource app."""

from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Note, Subject, Taught, Book, Syllabus, Topic, WebTutorial, VideoTutorial, QuestionPaper
from .forms import BookForm, DepartmentSemesterForm, NoteForm, QuestionPaperForm, VideoTutorialForm, WebTutorialForm

class HomeView(TemplateView):

    '''View for home route.'''
    
    #Only get method is acceptable.
    http_method_names = ['get']

    def get_template_names(self):
        '''Return the template to render.'''

        template_name = 'resources/home.html'

        #If user is signed in then show the dashboard.
        if self.request.user.is_authenticated:
            template_name = 'resources/dashboard.html'
        return template_name


class SyllabusView(LoginRequiredMixin, TemplateView):

    '''View to download syllabus.'''

    template_name = 'resources/syllabus.html'

    def get(self, request, *args, **kwargs):
        ''' Handles the get request.'''

        dept_name = request.user.get_department(request)
        semester = request.user.get_semester(request)
        if dept_name is None or semester is None:
            #Prompt user to choose department and semester in form as they are not available.
            msg = "Choose your department and semester."
            messages.warning(request, msg)
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        ''' Handles the post request, when user fill the department and semester form.'''

        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')

        #Set the session variable for future use case.
        request.session['dept_name'] = dept_name
        request.session['semester'] = semester

        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, dept_name: str, semester: int, **kwargs) -> dict:
        '''Add the extra context data(form, link, breadcrumbs) to context dict and return it.'''

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

    '''Show the list of resources available to select and then redirect to selected resource url.'''

    template_name = "resources/resources.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        ''' Get the context data to render on template.'''

        #Get parent context dictionary
        context = super().get_context_data(**kwargs)

        #Add all resources name to show and their route to redirect
        views = ['notes', 'books', 'online_tutorials', 'question_papers']
        views_list = []
        for view in views:
            views_list.append({'view_name':view, 'view_url':reverse(view)})
        context['views'] = views_list

        return context

class SubjectView(LoginRequiredMixin, TemplateView):

    '''View to show the list of subjects and redirect to show coresponding resource.'''

    template_name = "resources/subjects.html"

    def get(self, request, **kwargs: dict):
        '''Handles the get request to show subjects.'''

        dept_name = request.user.get_department(request)
        semester = request.user.get_semester(request)
        if dept_name is None or semester is None:
            #Propmt user to choose department and semester as it is not available.
            msg = "Choose department and semester to see subjects."
            messages.warning(request, msg)
        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs: dict):
        '''Handles the post request to show subjects( happens when user submit
        department_semester form.
        '''

        dept_name = request.POST.get('dept_name')
        semester = request.POST.get('semester')

        #Set the department and semester in session variable for future reference.
        request.session['dept_name'] = dept_name
        request.session['semester'] = semester

        context = self.get_context_data(dept_name, semester, **kwargs)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, dept_name, semester, **kwargs) -> dict:
        ''' Get the context data for subject view.'''

        #Get Parent's context data.
        context = super().get_context_data(**kwargs)

        #Add DepartmentSemeter Form
        form_data = {'dept_name': dept_name, 'semester': semester}
        context['form'] = DepartmentSemesterForm(data=form_data)

        #All subject taught in current department and semester.
        context['subjects'] = Taught.get_subjects(dept_name= dept_name, semester=semester)

        #Url to redirect after user select a subject.
        next_url = self.kwargs.get('next_url')
        context['next_url'] = next_url

        #Breadcrumbs of page.
        context['breadcrumbs'] = {'Home': reverse('home'), next_url: 'None'}

        return context


class ResourceAbstractView(LoginRequiredMixin, TemplateView):

    ''' Abstract class to show all available resources of a subject.
    
    All view to show resources inherits from this view and override the get_context_data() method to pass
    extra data.'''

    def get(self, request, **kwargs):
        ''' Handles the get request of route.'''

        #Catch sub_code from url parameter.
        sub_code = self.kwargs.get('sub_code', None)
        
        if sub_code is None:
            #Redirect to pick a subject first.
            return redirect(to='subjects', next_url = self.url)
        else:
            #Show all resources by passing in context dict.
            context = self.get_context_data(**kwargs)
            return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs) -> dict:
        '''Provides the basic data to render on all resources page. All ResourceView 
        inheriting this class should provide the list of resources by overriding this method.'''

        #Get the parent class context data.
        context = super().get_context_data(**kwargs)

        #Try to capture sub_code from url.
        sub_code = self.kwargs.get('sub_code')

        #Error message if subject is not available whoose code match with sub_code.
        error_message = None

        if sub_code is None:
            #Page will be redirected to subject as sub_code is none and after selcting
            #subject, it will come to this page again.
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

    ''' View to show OnlineTutorials '''

    template_name = "resources/online_tutorials.html"
    url = "online_tutorials"

    def get_context_data(self, **kwargs) -> dict:
        '''Context data to pass in template.
        
        Get the basic data in context dict from parent class and 
        add list of video tutorials and web tutorials in it if available.
        '''
        
        #Get basic data from parent class.
        context = super().get_context_data(**kwargs)
        
        #Add resources if subject exist i.e there is no error.
        if not context['error']:
            #Capture sub_code from url.
            sub_code = self.kwargs.get('sub_code')
            #Tutorial's lists.
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

    ''' View to show Books '''

    template_name = "resources/books.html"
    url = "books"

    def get_context_data(self, **kwargs) -> dict:
        '''Context data to pass in template.
        
        Get the basic data in context dict from parent class and 
        add list of Books in it if available.
        '''
        
        #Get basic data from parent class.
        context = super().get_context_data(**kwargs)

        #Add resources if subject exist i.e there is no error.
        if not context['error']:
            #Capture sub_code from url.
            sub_code = self.kwargs.get('sub_code')
            #Book's lists.
            books = Book.get_books(sub_code=sub_code)
            if not books:
                error_message = "Books are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['books'] = books
        return context


class NoteView(ResourceAbstractView):

    ''' View to show Notes.'''

    template_name = "resources/notes.html"
    url = 'notes'

    def get_context_data(self, **kwargs) -> dict:
        '''Context data to pass in template.
        
        Get the basic data in context dict from parent class and 
        add list of Notes in it if available.
        '''
        
        #Get basic data from parent class.
        context = super().get_context_data(**kwargs)

        #Add resources if subject exist i.e there is no error.
        if not context['error']:
            #Capture sub_code from url.
            sub_code = self.kwargs.get('sub_code')
            #Note's lists.
            notes = Note.get_all_notes(sub_code=sub_code)
            if not notes:
                error_message = "Notes are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['notes'] = notes
        return context


class QuestionPaperView(ResourceAbstractView):

    ''' View to show QuestionPapers.'''

    template_name = "resources/question_papers.html"
    url = "question_papers"

    def get_context_data(self, **kwargs) -> dict:
        '''Context data to pass in template.
        
        Get the basic data in context dict from parent class and 
        add list of QuestionPaper in it if available.
        '''
        
        #Get basic data from parent class.
        context = super().get_context_data(heading="Question Papers", **kwargs)

        #Add resources if subject exist i.e there is no error.
        if not context['error']:
            #Capture sub_code from url.
            sub_code = self.kwargs.get('sub_code')
            #Question Paper's lists.
            question_papers = QuestionPaper.get_question_papers(sub_code=sub_code)
            if not question_papers:
                error_message = "Question Papers are not available now, but will be uploaded soon."
                context['error'] = error_message
            else:
                context['question_papers'] = question_papers
        return context

class ContributeView(ResourceListView):
    '''View to show the list of resources user can contribute.'''
    
    def get_context_data(self, **kwargs):
        '''Context data to pass in template.
        Return the list of dict where each dict contain name of contribute-resource and url
        of contribute-resource.'''

        #List of resource views user can contribute.
        views = ['contribute-notes', 'contribute-question_papers', 'contribute-books', 
        'contribute-video_tutorials', 'contribute-web_tutorials']
        view_name = ['Note', 'Question Paper', 'Book', 'VideoTutorial', 'WebTutorial']
        views_list = []
        for i in range(len(views)):
            views_list.append({'view_name':view_name[i], 'view_url':reverse('subjects',kwargs= {'next_url':views[i]})})
        context = {'views' : views_list}
        return context

class ContributeFormView(LoginRequiredMixin, CreateView):

    '''Abstract contribute view.
    
    All contribute-resource view inherites this class.'''

    def form_valid(self, form):
        '''Method calls after form is valid.
        
        Add the contributor in model instance as current user and call's parent form valid.'''

        form.instance.contributor = self.request.user
        msg = "Your request is submitted succesfully. After a succesfull review by our team, this will be uploaded. Thanks!"
        messages.success(self.request, msg)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        ''' Handles get request.'''

        #User can not contribute. so, redirect to main contribute page.
        if not request.user.can_contribute():
            msg = f'''You have contributed {request.user.contribution_limit} items which are not 
            verified yet.Once they are verified, you will be egligble to contribute again. Till then, Wait!'''
            messages.warning(request, msg)
            return redirect(to='contribute')
        return super().get(request, *args, **kwargs)


class ContributeNoteView(ContributeFormView):
    '''View to contribute notes.'''

    model = Note
    form_class = NoteForm
    template_name = "resources/contribute_notes.html"
    #Redirect user on main contribute menu after contribution.
    success_url = reverse_lazy('contribute')

    def form_valid(self, form):
        '''Method calls after form is valid.'''
        try:
            Note.objects.get(topic__name=form.cleaned_data['topic'])
        except Note.DoesNotExist:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You already have uploaded notes for this topic.')
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        ''' Get the note form and modify topic's querset to contain only particular subject's topic.'''

        form = super().get_form(form_class=form_class)
        topics = Topic.objects.filter(subject__code=self.kwargs['sub_code'])
        form.fields['topic'].queryset = topics
        return form


class ContributeQuestionPaperView(ContributeFormView):

    '''View to contribute QuestionPapers.'''

    model = QuestionPaper
    form_class = QuestionPaperForm
    template_name = "resources/contribute_question_paper.html"
    success_url = reverse_lazy('contribute')

    def get_form(self, form_class=None):
        ''' Get the QuestionPaper form and add subject field to it.'''

        #Get the form
        form = super().get_form(form_class=form_class)

        #Add subject's field initial value
        try:
            #Get subject from sub_code captured in url.
            subject = Subject.objects.get(code=self.kwargs['sub_code'])
        except Subject.DoesNotExist:
            subject = None
        finally:
            form['subject'].initial = subject
            
        return form



class ContributeBookView(ContributeFormView):

    '''View to contribute Books.'''

    model = Book
    form_class = BookForm
    template_name = "resources/contribute_books.html"
    success_url = reverse_lazy('contribute')

    def get_form(self, form_class=None):
        ''' Get the Book form and add subject field to it.'''

        #Get the form
        form = super().get_form(form_class=form_class)

        #Add subject's field initial value
        try:
            #Get subject from sub_code captured in url.
            subject = Subject.objects.get(code=self.kwargs['sub_code'])
        except Subject.DoesNotExist:
            subject = None
        finally:
            form['subject'].initial = subject
            
        return form



class ContributeVideoTutorialView(ContributeFormView):

    '''View to contribute VideoTutorials.'''

    model = VideoTutorial
    form_class = VideoTutorialForm
    template_name = "resources/contribute_video_tutorials.html"
    success_url = reverse_lazy('contribute')

    def get_form(self, form_class=None):
        ''' Get the VideoTutorial form and add subject field to it.'''

        #Get the form
        form = super().get_form(form_class=form_class)

        #Add subject's field initial value
        try:
            #Get subject from sub_code captured in url.
            subject = Subject.objects.get(code=self.kwargs['sub_code'])
        except Subject.DoesNotExist:
            subject = None
        finally:
            form['subject'].initial = subject
            
        return form



class ContributeWebTutorialView(ContributeFormView):

    '''View to contribute web tutorials.'''

    model = WebTutorial
    form_class = WebTutorialForm
    template_name = "resources/contribute_web_tutorials.html"
    success_url = reverse_lazy('contribute')

    def get_form(self, form_class=None):
        ''' Get the Webtutorial form and add subject field to it.'''

        #Get the form
        form = super().get_form(form_class=form_class)

        #Add subject's field initial value
        try:
            #Get subject from sub_code captured in url.
            subject = Subject.objects.get(code=self.kwargs['sub_code'])
        except Subject.DoesNotExist:
            subject = None
        finally:
            form['subject'].initial = subject

        return form


class TeamView(LoginRequiredMixin, TemplateView):

    '''Templat view to render team page.'''

    template_name = "resources/team.html"
