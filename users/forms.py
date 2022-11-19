from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from django.forms.widgets import PasswordInput, TextInput
from .models import Profile, Skill, Message, Social, Opportunity


# class CustomAuthForm(AuthenticationForm):
#     super(AuthenticationForm, self).__init__(*args, **kwargs)
#     username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
#     password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})


class ProfileForm(ModelForm):
    # radio buttons to choose profile type
    PROFILE_CHOICES = [('alum','JTC Alum'),('affiliate','Affiliate Organization')]
    
    profile_type = forms.CharField(label = 'Profile Type', required = True, widget = forms.RadioSelect(choices = PROFILE_CHOICES))
    github_update = forms.BooleanField(widget = forms.CheckboxInput())
    
    
    class Meta:
        model = Profile
        
        fields = ['name', 'email', 'username', 'location', 'profile_type', 'github_update', 'bio', 'short_intro', 'organization_name', 'profile_image']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        cnt = 0
        for name, field in self.fields.items():
            if 'profile_type' == field:
                cnt += 1;
                field.widget.attrs.update({'placeholder': field.label, 'class': 'input radio'})
            elif 'github_update' == field:
                field.widget.attrs.update({'class': 'input'})
            else:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})
            


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})


class SocialForm(ModelForm):    
    class Meta:
        model = Social
        fields = '__all__'
        exclude = ['css', 'id', 'account']
    
    def __init__(self, *args, **kwargs):
        super(SocialForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})


class OpportunityForm(ModelForm):    
    class Meta:
        model = Opportunity
        fields = ['title', 'company', 'body', 'weblink', 'poster']
    
    def __init__(self, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label, 'class': 'input'})