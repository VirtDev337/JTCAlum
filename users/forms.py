from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect
from .models import Profile, Skill, Message, Social


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    # radio buttons to choose profile type
    PROFILE_CHOICES = [('alum','JTC Alum'),('affiliate','Affiliate Organization')]
    profile_type = forms.CharField(label='Profile Type', required=True, widget=forms.RadioSelect(choices=PROFILE_CHOICES))
    class Meta:
        model = Profile
        
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_image', 'profile_type',]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SocialForm(ModelForm):    
    class Meta:
        model = Social
        fields = '__all__'
        exclude = ['css', 'id', 'account']
    
    def __init__(self, *args, **kwargs):
        super(SocialForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})