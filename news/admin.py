from django.contrib import admin
from .models import News, Comment, Category
from easy_select2 import select2_modelform
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    form = select2_modelform(News, attrs={'width': '250px'})




admin.site.register(News, NewsAdmin)
admin.site.register(Comment)
admin.site.register(Category)