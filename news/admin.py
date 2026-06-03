from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'created_date', 'is_active')
    list_filter = ('is_active', 'created_date')
