from django.db import models
from django.contrib.auth.models import User

# 1. USER PROFILE: Stores if someone is an Employer or Seeker
class UserProfile(models.Model):
    USER_ROLES = (
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 2. JOB: Stores the details of the job openings
class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title

# 3. APPLICATION: Connects a User to a Job
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_link = models.URLField()
    cover_letter = models.TextField(null=True, blank=True) 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"
    