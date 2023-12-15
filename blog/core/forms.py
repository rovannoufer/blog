from django.forms import ModelForm, widgets
from .models import Project
from django import forms

class BlogForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'intro', 'featured_image', 'description', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        # Update widget attributes for each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
