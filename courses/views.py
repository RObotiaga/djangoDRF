from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Lesson, Course

from .serializers import LessonSerializer, CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


################################################################
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = Lesson


class LessonListAPIView(generics.ListAPIView):
    serializer_class = Lesson
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = Lesson
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    get_queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = Lesson
    queryset = Lesson.objects.all()
