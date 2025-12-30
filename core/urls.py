"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from jobs.views import job_list,register,post_job# Import your new view here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', job_list, name='home'), # This makes it the home page
]

from django.contrib import admin
from django.urls import path, include # Add 'include'
from jobs.views import job_list, register,post_job,apply_job,my_applications,delete_job,view_applicants,toggle_job_status,edit_job,withdraw_application
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'), # New register link
    path('accounts/', include('django.contrib.auth.urls')), # Built-in login/logout
    path('post-job/', post_job, name='post_job'),
    path('', job_list, name='home'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('my-applications/', my_applications, name='my_applications'),
    path('job/<int:job_id>/delete/', delete_job, name='delete_job'),
    path('job/<int:job_id>/applicants/', view_applicants, name='view_applicants'),
    path('job/<int:job_id>/toggle/', toggle_job_status, name='toggle_job_status'),
path('job/<int:job_id>/edit/', edit_job, name='edit_job'),
# Add this to your urlpatterns in core/urls.py
path('application/<int:application_id>/withdraw/', withdraw_application, name='withdraw_application'),
]