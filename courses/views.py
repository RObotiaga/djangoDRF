from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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
            return Course.objects.all()
        return Course.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        serializer.save(user=self.request.user)


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


################################################################

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ()
    ordering_fields = ('course', 'lesson', 'payment_method', 'payment_date')


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
