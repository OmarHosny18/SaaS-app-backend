from django.contrib import admin
from .models import LessonCategory, Lesson, LessonProgress


@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'estimated_reading_time', 'created_by')
    list_filter = ('difficulty', 'category')
    search_fields = ('title',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed',)