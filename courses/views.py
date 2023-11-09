import requests
from decouple import config
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
import json
from datetime import datetime, timedelta
from .tasks import send_notification
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Lesson, Course, Payment, Subscription
from rest_framework.filters import SearchFilter, OrderingFilter

from .permissions import IsOwner, IsManager
from .serializers import LessonSerializer, CourseSerializer, PaymentSerializer, SubscriptionSerializer
from .pagination import CoursePagination


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderator').exists():
            return Course.objects.all().order_by('id')
        return Course.objects.filter(user=user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        send_notification.delay(course.pk)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner | IsAdminUser | IsManager, ]
        elif self.action == 'delete' or self.action == 'create':
            permission_classes = [IsOwner, ]
        elif self.action == 'list':
            permission_classes = [IsOwner | IsAdminUser, ]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


################################################################
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsAdminUser | IsManager, ]

    def perform_create(self, serializer):
        lesson = serializer.save(user=self.request.user)
        send_notification.delay(lesson.course.id)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(user=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser, ]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]

    def perform_update(self, serializer):
        lesson = serializer.save()
        send_notification.delay(lesson.course.id)


################################################################

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ()
    ordering_fields = ('course', 'lesson', 'payment_method', 'payment_date')


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_403_FORBIDDEN)

        amount = request.data['amount']
        payment_method = request.data['payment_method']
        course = request.data.get('course')
        lesson = request.data.get('lesson')
        user = self.request.user
        stripe_secret_key = config('STRIPE_SECRET_KEY')
        stripe_api_url = "https://api.stripe.com/v1/payment_intents"

        headers = {
            "Authorization": f"Bearer {stripe_secret_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "amount": int(amount) * 100,  # Сумма в центах
            "currency": "usd",  # Валюта
        }

        try:
            response = requests.post(stripe_api_url, headers=headers, data=data)
            payment_intent = response.json()
            new_payment = Payment.objects.create(
                amount=amount,
                payment_method=payment_method,
                user=user,
                key=payment_intent.get('client_secret'),
                course=course,
                lesson=lesson,
            )
            new_payment.save()
            return Response({"client_secret": payment_intent.get('client_secret'),
                             "payment_method": payment_intent.get('payment_method')})

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]


################################################################

class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderator').exists():
            return Subscription.objects.all()
        return Subscription.objects.filter(user=user)


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwner | IsAdminUser | IsManager, ]
