from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from users.models import Profile
from django.urls import reverse
from django.conf import settings
import os
# Create your models here.


class Project(models.Model):
    # Project specific attributes
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
    owner = models.ForeignKey(Profile, null = True, blank = True, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    slug = models.SlugField(default = '', editable = False, max_length = 200, null = False)
    created = models.DateTimeField(auto_now_add = True)
    description = models.TextField(null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True)
    featured_image = models.ImageField(null = True, blank = True, 
                                        upload_to = 'projects/', default = "projects/default.jpg")
    
    # Project specific Links
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.CharField(max_length = 2000, null = True, blank = True)
    
    # Demo and sub-site attributes
    site = models.ForeignKey(Site, default = None, on_delete=models.CASCADE)
    demo = models.BooleanField(default = False, null = True, blank = True)
    demo_set = models.BooleanField(default = False, null = True, blank = True)
    
    # Information of the project directory structure if demoed
    project_name = models.CharField(max_length = 200, default = "", blank = True, null = True)
    site_name = models.CharField(max_length = 200, default = "", blank = True, null = True)
    project_directory = models.CharField(max_length = 200, default = "", blank = True, null = True)
    site_directory = models.CharField(max_length = 200, default = "", blank = True, null = True)
    
    # Review
    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
        unique_together = [['slug', 'owner']]

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value = 'up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    
    def get_absolute_url(self):
        kwargs = {
            'slug' : self.slug,
            'name' : self.owner.slug,
        }
        
        return reverse('user-profile', kwargs = kwargs)
    
    def save(self, *args, **kwargs):
        self.slug = slugify( self.title)
        self.project_name = self.slug if not self.project_name else self.project_name
        
        if self.demo:
            self.project_directory = os.path.join(settings.DEMOS_ROOT, f'{self.owner.slug}/{self.project_directory}') if self.project_directory != '' and '/' not in self.project_directory  else os.path.join(settings.DEMOS_ROOT, f'{self.owner.slug}/{self.project_name}')
            
            self.site_directory = os.path.join(self.project_directory, self.site_directory) if self.site_directory != '' else os.path.join(self.project_directory, self.site_name)
            
            self.site.domain = '{settings.PARENT_HOST}/{self.owner.slug}/{self.slug}'
            self.site.name = '{self.owner.slug}-{self.slug}'
        
        super().save(*args, **kwargs)


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True)
    
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField(null = True, blank = True)
    
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    
    created = models.DateTimeField(auto_now_add = True)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length = 200)
    
    created = models.DateTimeField(auto_now_add = True)
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.name
