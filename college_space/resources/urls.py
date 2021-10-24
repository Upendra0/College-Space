"""resources URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(views.'', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', view=views.HomeView.as_view(), name='home'),
    path('syllabus', view=views.SyllabusView.as_view(), name='syllabus'),
    path('resources', view=views.ResourceListView.as_view(), name='resources'),
    path('subjects/<next_url>', view=views.SubjectView.as_view(), name='subjects'),
    path('books', view=views.BookView.as_view(), name='books'),
    path('books/<sub_code>', view=views.BookView.as_view(), name='books'),
    path('notes', view=views.NoteView.as_view(), name='notes'),
    path('notes/<sub_code>', view=views.NoteView.as_view(), name='notes'),
    path('online_tutorials', view=views.OnlineTutorialView.as_view(), name='online_tutorials'),
    path('online_tutorials/<sub_code>', view=views.OnlineTutorialView.as_view(), name='online_tutorials'),
    path('question_papers', view=views.QuestionPaperView.as_view(), name='question_papers'),
    path('question_papers/<sub_code>', view=views.QuestionPaperView.as_view(), name='question_papers'),
    path('team', view=views.TeamView.as_view(), name='team'),
    path('contribute', view=views.ContributeView.as_view()),
    path('contribute/notes', view=views.ContributeNoteView.as_view(), name='contribute-notes'),
    path('contribute/question_papers', view=views.QuestionPaperView.as_view(), name='contribute-question_paper'),
    
]
