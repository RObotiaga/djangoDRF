from django.contrib import admin
from .models import Course, Lesson


# Register your models here.
@admin.register(Course)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Lesson)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description')
    list_filter = ('name',)
    search_fields = ('name',)
