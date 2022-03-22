from django.db import models
from django.contrib.auth.models import User
import uuid
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, 
                                null = True, blank = True)
    name = models.CharField(max_length = 200, blank = True, null = True)
    email = models.EmailField(max_length = 500, blank = True, null = True)
    username = models.CharField(max_length = 200, blank = True, null = True)
    location = models.CharField(max_length = 200, blank = True, null = True)
    
    short_intro = models.CharField(max_length = 200, blank = True, null = True)
    bio = models.TextField(blank = True, null = True)
    profile_image = models.ImageField(null = True, blank = True, 
                            upload_to = 'profiles/', 
                            default = "profiles/user-default.png")
    
    collaborators = models.ForeignKey('Profile', on_delete = models.CASCADE, 
                                        null = True, blank = True)
    
    social_github = models.CharField(default = '', max_length = 200, blank = True, null = True)
    social_twitter = models.CharField(default = '', max_length = 200, blank = True, null = True)
    social_linkedin = models.CharField(default = '', max_length = 200, blank = True, null = True)
    social_youtube = models.CharField(default = '', max_length = 200, blank = True, null = True)
    social_website = models.CharField(default = '', max_length = 200, blank = True, null = True)

    created = models.DateTimeField(auto_now_add = True)
    
    slug = models.SlugField(default = '', editable = False, max_length = 200, null = False)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                        primary_key = True, editable = False)

    def __str__(self):
        return str(self.username)

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
        self.slug = slugify(self.name)
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
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Social(models.Model):
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                        primary_key = True, editable = False)
    
    account = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    
    github = models.CharField(default = '', max_length = 200, blank = True, null = True)
    twitter = models.CharField(default = '', max_length = 200, blank = True, null = True)
    linkedin = models.CharField(default = '', max_length = 200, blank = True, null = True)
    youtube = models.CharField(default = '', max_length = 200, blank = True, null = True)
    website = models.CharField(default = '', max_length = 200, blank = True, null = True)
    
    def __str__(self):
        return str(self.account)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete = models.SET_NULL, 
                                null = True, blank = True)
    recipient = models.ForeignKey(Profile, on_delete = models.SET_NULL, 
                            null = True, blank = True, related_name = "messages")
    
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
