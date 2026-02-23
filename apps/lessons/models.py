from django.db import models
from apps.accounts.models import CustomUser


class LessonCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Lesson Categories'

    def __str__(self):
        return self.name

class Lesson(models.Model):

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        LessonCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    estimated_reading_time = models.IntegerField(help_text='Time in minutes')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name_plural = 'Lesson Progresses'

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"