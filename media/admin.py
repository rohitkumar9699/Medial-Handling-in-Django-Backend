from django.contrib import admin
from .models import Media
# admin.site.register(Media)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'file', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

