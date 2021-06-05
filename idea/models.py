from config.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import  reverse
from ckeditor_uploader.fields import RichTextUploadingField
from news.models import Category


class Idea(models.Model):

    class Meta:
        permissions = [
            ('all', 'all of the permissions')
        ]
        ordering = ['-datetime']

    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/idea/header/")
    body = RichTextUploadingField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ManyToManyField(Category, related_name='category_idea')
    like_idea = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='the_like')
    unlike_idea = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='the_like_unlike')

    def total_likes(self):
        return self.like_idea.count()

    def total_unlikes(self):
        return self.unlike_idea.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("idea:idea_detail", args=[str(self.id)])


class CommentIdea(models.Model):
    idea = models.ForeignKey(
        Idea, 
        on_delete=models.CASCADE,
        related_name='comments_idea',
        )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    comment_idea = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)

    like_comment_idea = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comment_idea_like')
    unlike_comment_idea = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comment_idea_unlike')

    def total_likes_comment(self):
        return self.like_comment_idea.count()

    def total_unlikes_comment(self):
        return self.unlike_comment_idea.count()

    class Meta:
        ordering = ['-created_on']
    

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment_idea, self.author)

    def get_absolute_url(self):
        return reverse('idea:idea_detail', args=[str(self.idea.id)])





