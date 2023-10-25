from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    url = models.URLField()

