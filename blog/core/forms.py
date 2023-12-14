from django.forms import ModelForm, widgets
from .models import Project
from django import forms

class BlogForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','intro', 'featured_image','description','tags']
        widgets = {
            'tags' : forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add title . . .'})
        self.fields['intro'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Introduction . . .'})
        self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Description . . .'})
       
