from django.contrib import admin
from .models import Idea, CommentIdea
from easy_select2 import select2_modelform


class CommentInline(admin.TabularInline):
    model = CommentIdea
    extra = 0


class IdeaAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    readonly_fields = ["datetime",]
    form = select2_modelform(Idea, attrs={'width': '250px'})




admin.site.register(Idea, IdeaAdmin)
admin.site.register(CommentIdea)