from rest_framework import serializers
from .models import Course, Lesson, Payment, Subscription


def youtube_url(value):
    if 'youtube.com' not in value:
        raise serializers.ValidationError("Ссылка должна вести на youtube")


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, required=False)

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'user']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'