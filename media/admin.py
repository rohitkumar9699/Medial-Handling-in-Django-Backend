from django.contrib import admin
from .models import Media, Marks, Students
# admin.site.register(Media)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'file', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Marks._meta.fields]
    ordering = ['roll']

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Students._meta.fields]
    ordering = ['roll']
