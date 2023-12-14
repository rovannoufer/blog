from django.forms import ModelForm
from .models import Project

class BlogForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','intro','description','tags']