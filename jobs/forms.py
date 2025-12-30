from django import forms
from .models import Job, Application

# 1. Form for Employers to post jobs
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# 2. Form for Seekers to apply for jobs
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['phone_number','resume_link', 'cover_letter'] # Both fields included now
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. +91 9876543210'
            }),
            'resume_link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://drive.google.com/your-resume'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Tell the employer why you are a good fit...', 
                'rows': 4
            }),
        }