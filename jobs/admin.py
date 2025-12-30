from django.contrib import admin
from .models import UserProfile, Job, Application

admin.site.register(UserProfile)
admin.site.register(Job)
admin.site.register(Application)