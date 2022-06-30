from django.forms import ModelForm
from django import forms
from .models import Project, Review


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


class DemoForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'site_name', 'app_name', 'project_directory', 'app_directory', 'site_directory']

        widgets = {
            'project_name': forms.TextInput(attrs = {
                'placeholder': 'Project Name',}),
            'site_name': forms.Textarea(attrs = {
                'placeholder': 'Site Name',}),
            'app_name': forms.Textarea(attrs = {
                'placeholder': 'App Name',}),
            'project_directory': forms.Textarea(attrs = {
                'placeholder': 'Project Directory'}),
            'app_directory': forms.Textarea(attrs = {
                'placeholder': 'App Directory'}),
            'site_directory': forms.Textarea(attrs = {
                'placeholder': 'Site Directory'}),
            
        }
    
    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})