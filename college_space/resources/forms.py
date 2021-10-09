from django import forms
from .models import Department

class DepartmentSemesterForm(forms.Form):
    dept_choices = Department.all_department()
    dept_choices = [ (ele.get('name'), ele.get('name')) for ele in dept_choices]
    sem_choices = [1,2,3,4,5,6,7,8]
    sem_choices = [ (ele, ele) for ele in sem_choices]
    dept_name = forms.ChoiceField(choices=dept_choices)
    semester = forms.ChoiceField(choices=sem_choices)