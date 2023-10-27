from django.urls import path

from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonDestroyAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, PaymentListAPIView
app_name = CoursesConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-list'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-destroy'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
] + router.urls
