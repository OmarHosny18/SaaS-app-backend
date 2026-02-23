from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import JobApplication, Tag
from .serializers import (
    JobApplicationReadSerializer,
    JobApplicationWriteSerializer,
    TagSerializer
)
from .filters import JobApplicationFilter
from apps.accounts.permissions import IsOwner


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class JobApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = JobApplicationFilter
    search_fields = ['company_name', 'job_title']
    ordering_fields = ['applied_date', 'created_at']

    def get_queryset(self):
        return JobApplication.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobApplicationReadSerializer
        return JobApplicationWriteSerializer

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        cache.delete(f"dashboard_{self.request.user.id}")


class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = JobApplicationFilter

    def get_queryset(self):
        return JobApplication.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobApplicationReadSerializer
        return JobApplicationWriteSerializer

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f"dashboard_{self.request.user.id}")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"dashboard_{self.request.user.id}")