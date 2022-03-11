from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from datetime import datetime as dt


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
    Months = ['1', '2', '3', '4', '5',), ('6',), ('7',), ('8',), ('9',), ('10',), ('11',), ('12',),)]
    Years = [str(year) for year in range(2015, int(dt.now().year))]
    
    graduation_date_month = forms.DateField(widget = forms.SelectDateWidget(months = Months))
    graduation_date_year = forms.DateField(widget = forms.SelectDateWidget(years = Years))
    
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'enrolled', 'alumn',
                'location', 'bio', 'short_intro', 'profile_image',
                'social_github', 'social_linkedin', 'social_twitter',
                'social_youtube', 'social_website']

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
