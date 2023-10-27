from django.db import models
from users.models import CustomUser
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    user = models.ForeignKey(CustomUser, verbose_name='пользователь', on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью', **NULLABLE)
    slug = models.SlugField(unique=True, default='', verbose_name='url')
    video_url = models.URLField()

    user = models.ForeignKey(CustomUser, verbose_name='пользователь', on_delete=models.DO_NOTHING, default=1)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='курс', null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lesson, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Наличные'), ('transfer', 'Перевод')])
