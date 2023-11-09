from django.contrib import admin
from .models import Course, Lesson, Subscription


# Register your models here.
@admin.register(Course)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Lesson)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'course')
    list_filter = ('name',)
    search_fields = ('name',)

    def course(self, obj):
        return f'{obj.course.name} №{obj.course.id}' if obj.course.name else "N/A"

    course.short_description = 'Курс'


@admin.register(Subscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status')
    list_filter = ('user', 'course',)
    search_fields = ('user', 'course', 'status')
