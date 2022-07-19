from django.db import models
from django import forms
from django.contrib.auth.models import User
import uuid
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import pytz


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, 
                                null = True, blank = True)
    name = models.CharField(max_length = 200, blank = True, null = True)
    email = models.EmailField(max_length = 500, blank = True, null = True)
    username = models.CharField(max_length = 200, blank = True, null = True)
    location = models.CharField(default = 'USA', max_length = 200, blank = True, null = True)
    
    short_intro = models.CharField(max_length = 200, blank = True, null = True)
    bio = models.TextField(blank = True, null = True)
    profile_image = models.ImageField(null = True, blank = True, 
                            upload_to = 'profiles/', 
                            default = "profiles/user-default.png")
    
    profile_type = models.CharField(default='alum', max_length=200)
    
    organization_name = models.CharField(default = '', max_length = 200, blank = True, null = True)

    created = models.DateTimeField(auto_now_add = True)
    
    slug = models.SlugField(default = '', editable = False, max_length = 200, null = False)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                        primary_key = True, editable = False)
    
    def __str__(self):
        if self.profile_type == 'alum':
            return str(self.name)
        else:
            return str(self.organization_name)
    
    class Meta:
        ordering = ['created']
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
    def save(self, *args, **kwargs):
        slug = self.name if self.profile_type == 'alum' else self.organization_name
        self.slug = slugify(slug)
        super().save(*args, **kwargs)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, 
                                null = True, blank = True)
    
    name = models.CharField(max_length = 200, blank = True, null = True)
    description = models.TextField(null = True, blank = True)
    
    created = models.DateTimeField(auto_now_add = True)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                        primary_key = True, editable = False)
    
    def __str__(self):
        return str(self.name)


class Social(models.Model):    
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                        primary_key = True, editable = False)
    
    account = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    
    name = models.CharField(default = '', max_length = 200, blank = True, null = True)
    
    url = models.URLField(default = '', max_length = 300)
    
    css = models.CharField(default = '', max_length = 50, editable = True, blank = True, null = True)
    
    class Meta:
        ordering = ['account', 'name']
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        css = self.name.lower()
        self.name = css
        if self.name in ['github', 'linkedin', 'twitter', 'stackoverflow', 'facebook', 'google']:
            css = f'im im-{self.name}'
        else:
            css = 'im im-globe' 
        
        self.css = css
        super().save(*args, **kwargs)


# class Collaborator(models.Model):
#     id = models.UUIDField(default = uuid.uuid4, unique = True, 
#                         primary_key = True, editable = False)
    
#     developer = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    
    # try:
    #     student = models.Student.objects.get(name="abc")
    # except:
    #     student = None  
    
    # students = models.Student.objects.filter(name="abc")
    
    # if student:
    #     print student.id
    # else:
    #     if students:
    #         print "There are multiple users with this name"
    #     else:
    #         print "The user doesn't exist"
    
    
    # people = []
    # for person in Profile.objects.exclude(user = developer.name).orderby('name'):
    #     people.append(person.name)
    
    # name = models.CharField(widget = CheckboxSelectMultiple(), choices = people, default = '', max_length = 300, blank = True, null = True)
    
    # def __str__(self):
    #     return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete = models.SET_NULL, null = True, blank = True)
    recipient = models.ForeignKey(Profile, on_delete = models.SET_NULL, null = True, blank = True, related_name = "messages")
    
    name = models.CharField(max_length = 200, null = True, blank = True)
    email = models.EmailField(max_length = 200, null = True, blank = True)
    
    subject = models.CharField(max_length = 200, null = True, blank = True)
    body = models.TextField()
    
    is_read = models.BooleanField(default = False, null = True)
    
    created = models.DateTimeField(auto_now_add = True)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True,
                        primary_key = True, editable = False)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created']


class Opportunity(models.Model):
    owner = models.ForeignKey(Profile, related_name='owner', on_delete = models.SET_NULL, null = True, blank = True)
    read = models.ForeignKey(Profile, related_name='read', on_delete = models.CASCADE, null = True, blank = True)
    
    poster = models.CharField(max_length = 200, null = True, blank = True)
    title = models.CharField(blank=False, null=True, max_length= 200)
    company = models.CharField(blank=False, null=True, max_length= 200)
    body = models.TextField(blank=False, null=True, max_length=7000)
    weblink = models.URLField(default = '', max_length = 400, blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True)    
    
    slug = models.SlugField(default = '', editable = False, max_length = 200, null = False)    
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
    
    class Meta:
        ordering = ['-created']
        unique_together = [['company', 'title']]
        # ordering = ['is_read', '-created']
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.company} {self.title}")
        super().save(*args, **kwargs)
