from django.urls import path
from .views import (
    LessonListView,
    LessonCreateView,
    LessonCategoryListView,
    UserProgressView,
    LessonDetailView,
    LessonUpdateDeleteView,
    MarkLessonCompleteView
)

urlpatterns = [
    path('', LessonListView.as_view(), name='lesson-list'),
    path('create/', LessonCreateView.as_view(), name='lesson-create'),
    path('categories/', LessonCategoryListView.as_view(), name='lesson-categories'),
    path('progress/', UserProgressView.as_view(), name='user-progress'),
    path('<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('<int:pk>/edit/', LessonUpdateDeleteView.as_view(), name='lesson-edit'),
    path('<int:pk>/complete/', MarkLessonCompleteView.as_view(), name='lesson-complete'),
]