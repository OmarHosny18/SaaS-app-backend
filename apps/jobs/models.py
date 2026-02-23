from django.db import models
from apps.accounts.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('wishlist', 'Wishlist'),
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    job_url = models.URLField(blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wishlist')
    applied_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    resume_version = models.CharField(max_length=100, blank=True)
    cover_letter_version = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class ResumeFeedback(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='feedback')
    resume_text = models.TextField()
    feedback_text = models.TextField()
    score = models.PositiveIntegerField(null=True, blank=True)
    rated_useful = models.BooleanField(null=True, blank=True)
    source = models.CharField(max_length=50, default='openai')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.job_application}"