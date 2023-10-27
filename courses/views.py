from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Lesson, Course, Payment
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import LessonSerializer, CourseSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


################################################################
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


################################################################

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ()
    ordering_fields = ('course', 'lesson', 'payment_method', 'payment_date')
