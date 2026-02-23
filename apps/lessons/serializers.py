from rest_framework import serializers
from .models import Lesson, LessonCategory, LessonProgress


class LessonCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonCategory
        fields = ('id', 'name')


class LessonListSerializer(serializers.ModelSerializer):
    category = LessonCategorySerializer(read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'category', 'difficulty', 'estimated_reading_time', 'is_completed')

    def get_is_completed(self, obj):
        if hasattr(obj, 'user_progress') and obj.user_progress:
            return obj.user_progress[0].completed
        return False


class LessonDetailSerializer(serializers.ModelSerializer):
    category = LessonCategorySerializer(read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_is_completed(self, obj):
        if hasattr(obj, 'user_progress') and obj.user_progress:
            return obj.user_progress[0].completed
        return False


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ('created_by',)


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('lesson', 'completed', 'completed_at')


class UserProgressSummarySerializer(serializers.Serializer):
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    completion_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    completed_lesson_ids = serializers.ListField(child=serializers.IntegerField())