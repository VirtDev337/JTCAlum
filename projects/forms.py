from django.forms import ModelForm
from django import forms
from .models import Project, Review
from django.contrib.sites.models import Site


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description',
                    'demo', 'source_link', 'demo_link']
        
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'demo': forms.CheckboxInput(),
            'title': forms.TextInput(attrs = {
                'placeholder': 'Title',}),
            'description': forms.Textarea(attrs = {
                'placeholder': 'Description',}),
            'source_link': forms.TextInput(attrs = {
                'placeholder': 'Source URL',}),
            'demo_link': forms.TextInput(attrs = {
                'placeholder': 'Demo URL',}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs = {
                'placeholder': 'Site Name'}),
            'domain': forms.TextInput(attrs = {
                'placeholder': 'Domain URI',
                'hint': 'Fully qualified domain name'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class DemoForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name', 
            'site_name', 
            'project_directory', 
            'site_directory']

        widgets = {
            'project_name': forms.TextInput(attrs = {
                'placeholder': 'Project Name',
                'hint': 'The project name as it appears on Github.'}),
            'site_name': forms.Textarea(attrs = {
                'placeholder': 'Site Name',
                'hint': 'The directory name as listed in the project directory.'}),
            'project_directory': forms.Textarea(attrs = {
                'placeholder': 'Project Directory',
                'hint': 'The name of the project root directory, which contains manage.py.  Define only if the directory is named differently than Project Name. '}),
            'site_directory': forms.Textarea(attrs = {
                'placeholder': 'Site Directory',
                'hint': 'The name of the site directory'}),
            
        }
    
    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})