from django.urls import path

from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonDestroyAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, PaymentListAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
urlpatterns = [
                  path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-destroy'),
                  path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
                  path('payment/<int:pk>', PaymentRetrieveAPIView.as_view(), name='payment-get'),
                  path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
                  path('course/subscript/', SubscriptionListAPIView.as_view(), name='subscription-list'),
                  path('course/subscript', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
                  path('course/subscript/<int:pk>', SubscriptionRetrieveAPIView.as_view(), name='subscription-get'),
                  path('course/subscript/<int:pk>', SubscriptionDestroyAPIView.as_view(), name='subscription-destroy'),
              ] + router.urls
