from django.contrib import admin
from .models import Tag, JobApplication, ResumeFeedback


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'user', 'status', 'applied_date', 'is_active')
    list_filter = ('status', 'is_active')
    search_fields = ('job_title', 'company_name')


@admin.register(ResumeFeedback)
class ResumeFeedbackAdmin(admin.ModelAdmin):
    list_display = ('job_application', 'score', 'source', 'created_at')