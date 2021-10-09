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

from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.home, name='home'),
    path('subjects', view=views.subjects, name='subjects'),
    path('syllabus', view=views.syllabus, name='syllabus'),
    path('videos', view=views.video_tutorials, name='videos'),
    path('notes', view=views.notes, name='notes'),
    path('reading_tutorials', view=views.reading_tutorials, name='reading_tutorials'),
    path('question_papers', view=views.question_papers, name='question_papers'),
    path('get_department_semester/<next_url>', view=views.get_department_semester, name='get_department_semester'),
]
