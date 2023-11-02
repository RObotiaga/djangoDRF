from rest_framework import serializers
from .models import Course, Lesson, Payment, Subscription
from .validators import youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, required=False)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj, status='sub').exists()
        return False
    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
