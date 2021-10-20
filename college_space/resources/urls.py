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
    path('books/<sub_code>', view=views.books, name='books'),
    path('notes/<sub_code>', view=views.notes, name='notes'),
    path('online_tutorials/<sub_code>', view=views.online_tutorials, name='online_tutorials'),
    path('question_papers/<sub_code>', view=views.question_papers, name='question_papers'),
    path('get_department_semester/<next_url>', view=views.get_department_semester, name='get_department_semester'),
    path('team', view=views.team, name='team'),
    #path('contribute', view=views.contribute)
]
