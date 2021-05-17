from django.contrib import admin
from .models import News, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]




admin.site.register(News, NewsAdmin)
admin.site.register(Comment)