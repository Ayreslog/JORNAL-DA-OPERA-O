from django.contrib import admin
from .models import Issue, PageImage

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'week_number', 'start_date', 'end_date', 'created_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    list_display = ('issue', 'page_number', 'image')