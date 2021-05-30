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
    readonly_fields = ["datetime",]
    form = select2_modelform(News, attrs={'width': '250px'})

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['slug',]
    search_fields = ['slug',]




admin.site.register(News, NewsAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Google_News)