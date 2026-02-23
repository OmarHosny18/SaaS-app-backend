from django.urls import path
from .views import (
    TagListCreateView,
    JobApplicationListCreateView,
    JobApplicationDetailView
)

urlpatterns = [
    path('', JobApplicationListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobApplicationDetailView.as_view(), name='job-detail'),
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
]