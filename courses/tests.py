from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Course, Lesson, Payment, Subscription
from users.models import CustomUser


class CourseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='admin@gmail.com', password='testpassword', phone='123')
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        data = {
            'name': 'Test Course',
            'description': 'Test Description',
        }
        response = self.client.post('/courses/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'Test Course')

    def test_update_course(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        data = {
            'name': 'Updated Course',
            'description': 'Updated Description',
        }
        response = self.client.put(f'/courses/{course.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        course.refresh_from_db()
        self.assertEqual(course.name, 'Updated Course')

    def test_delete_course(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        response = self.client.delete(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)


class LessonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='admin@gmail.com', password='testpassword', phone='123', )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        data = {
            'name': 'Test Lesson',
            'description': 'Test Content',
            'video_url': 'https://www.youtube.com/',
            'course': str(course.id),
        }
        response = self.client.post(reverse("courses:lesson-create"), data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().name, 'Test Lesson')

    def test_update_lesson(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        lesson = Lesson.objects.create(name='Test Lesson', description='Test Content', video_url='https://www.youtube.com/', course=course)
        data = {
            'name': 'Test update Lesson',
            'description': 'Test update Content',
            'video_url': 'https://www.youtube.com/',
            'course': str(course.id),
        }
        response = self.client.put(reverse("courses:lesson-update", args=(lesson.id,)), data, format='json')
        self.assertEqual(response.status_code, 200)
        lesson.refresh_from_db()
        self.assertEqual(lesson.name, 'Test update Lesson')

    def test_delete_lesson(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        lesson = Lesson.objects.create(name='Test Lesson', description='Test Content', video_url='https://www.youtube.com/', course=course)
        response = self.client.delete(reverse("courses:lesson-destroy", args=(lesson.id,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='admin@gmail.com', password='testpassword', phone='123')
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        data = {
            'course': course.id,
        }
        response = self.client.post(reverse('courses:subscription-create'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get().user, self.user)
        self.assertEqual(Subscription.objects.get().course, course)

    def test_list_subscriptions(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        subscription = Subscription.objects.create(course=course, user=self.user)
        response = self.client.get(reverse('courses:subscription-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
        self.assertEqual(response.data[0]['course'], course.id)

    def test_delete_subscription(self):
        course = Course.objects.create(name='Test Course', description='Test Description', user=self.user)
        data = {
            'course': course.id,
        }
        self.client.post(reverse('courses:subscription-create'), data, format='json')
        response = self.client.delete(reverse('courses:subscription-destroy', args=(1,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscription.objects.count(), 0)
