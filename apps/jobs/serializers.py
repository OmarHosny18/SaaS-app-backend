from rest_framework import serializers
from .models import JobApplication, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class JobApplicationReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'


class JobApplicationWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = JobApplication
        exclude = ('user',)

    def validate(self, data):
        if 'user' in data:
            raise serializers.ValidationError(
                'You cannot assign or reassign the user field directly.'
            )
        return data

    def _handle_tags(self, instance, tags_data):
        tag_objects = []
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            tag_objects.append(tag)
        instance.tags.set(tag_objects)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        self._handle_tags(instance, tags_data)
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags_data is not None:
            self._handle_tags(instance, tags_data)
        return instance