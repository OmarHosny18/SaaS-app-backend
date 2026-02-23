from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('jobs/', include('apps.jobs.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('lessons/', include('apps.lessons.urls')),
]