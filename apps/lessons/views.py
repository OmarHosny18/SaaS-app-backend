from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsAdminRole
from .models import Lesson, LessonCategory, LessonProgress
from .serializers import (
    LessonListSerializer,
    LessonDetailSerializer,
    LessonCreateSerializer,
    LessonCategorySerializer,
    LessonProgressSerializer,
    UserProgressSummarySerializer
)


def get_lesson_queryset(user):
    return Lesson.objects.prefetch_related(
        Prefetch(
            'lessonprogress_set',
            queryset=LessonProgress.objects.filter(user=user),
            to_attr='user_progress'
        )
    )


class LessonCategoryListView(generics.ListAPIView):
    queryset = LessonCategory.objects.all()
    serializer_class = LessonCategorySerializer
    permission_classes = [IsAuthenticated]


class LessonListView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = get_lesson_queryset(self.request.user)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__id=category)
        return qs


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_lesson_queryset(self.request.user)


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LessonUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class MarkLessonCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'detail': 'Lesson not found.'}, status=404)

        progress, _ = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)


class UserProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_lessons = Lesson.objects.count()
        completed_qs = LessonProgress.objects.filter(
            user=request.user,
            completed=True
        )
        completed_lessons = completed_qs.count()

        if total_lessons == 0:
            completion_percentage = Decimal('0.00')
        else:
            completion_percentage = Decimal(
                str(completed_lessons / total_lessons * 100)
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        completed_lesson_ids = list(completed_qs.values_list('lesson_id', flat=True))

        data = {
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'completion_percentage': completion_percentage,
            'completed_lesson_ids': completed_lesson_ids,
        }

        serializer = UserProgressSummarySerializer(data)
        return Response(serializer.data)