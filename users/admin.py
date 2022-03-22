from django.contrib import admin

# Register your models here.

from .models import Profile, Skill, Message, Social

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)
admin.site.register(Social)