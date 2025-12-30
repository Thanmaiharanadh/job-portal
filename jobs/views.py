from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Job, Application
from .forms import JobForm, ApplicationForm

# 1. Home Page with Search
def job_list(request):
    query = request.GET.get('search')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# 2. User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/register.html', {'form': form})

# 3. Post a New Job
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('home')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

# 4. Apply for a Job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f"Successfully applied for {job.title}!")
            return redirect('home')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_form.html', {'form': form, 'job': job})

# 5. Dashboard for Seekers
@login_required
def my_applications(request):
    user_apps = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/my_applications.html', {'applications': user_apps})

# 6. Dashboard for Employers (View Applicants)
@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Check if the user is the owner OR a staff/admin member
    if request.user == job.employer or request.user.is_staff:
        applicants = Application.objects.filter(job=job)
        return render(request, 'jobs/view_applicants.html', {'job': job, 'applicants': applicants})
    return HttpResponseForbidden("This applicant list is private.")

# 7. Toggle Job Status (Hiring vs Closed)
@login_required
def toggle_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    job.is_active = not job.is_active
    job.save()
    status_msg = "opened" if job.is_active else "closed"
    messages.success(request, f"Job '{job.title}' has been {status_msg}.")
    return redirect('home')

# 8. Delete a Job Posting
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job posting removed.")
        return redirect('home')
    return render(request, 'jobs/delete_confirm.html', {'job': job})
@login_required
def edit_job(request, job_id):
    # 1. First, find the job by its ID
    job = get_object_or_404(Job, id=job_id)
    
    # 2. SECURITY: Check if the user is the owner OR an admin
    if request.user == job.employer or request.user.is_staff:
        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, f"Changes saved for {job.title}!")
                return redirect('home')
        else:
            form = JobForm(instance=job)
        
        return render(request, 'jobs/post_job.html', {
            'form': form, 
            'edit_mode': True, 
            'job': job
        })
    else:
        # 3. If a regular user tries to edit someone else's job
        return HttpResponseForbidden("You are not authorized to edit this job.")
    @login_required
    def withdraw_application(request, application_id):
    # Find the application but ensure it belongs to the logged-in user
        application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == 'POST':
        job_title = application.job.title
        application.delete()
        messages.success(request, f"Your application for {job_title} has been withdrawn.")
        return redirect('my_applications')
        
    return render(request, 'jobs/withdraw_confirm.html', {'application': application})

# Add this to the bottom of jobs/views.py
@login_required
def withdraw_application(request, application_id):
    # This finds the application and ensures only the applicant can delete it
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, "Application withdrawn successfully.")
        return redirect('my_applications')
        
    return render(request, 'jobs/withdraw_confirm.html', {'application': application})