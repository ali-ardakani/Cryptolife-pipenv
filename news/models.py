from config.settings import AUTH_USER_MODEL
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import  reverse
from ckeditor.fields import  RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class News(models.Model):

    class Meta:
        permissions = [
            ('all', 'all of the permissions')
        ]
        ordering = ['-date']

    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/news/header/")
    body = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    like_news = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='the_news')
    unlike_news = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='the_news_unlike')

    def total_likes(self):
        return self.like_news.count()

    def total_unlikes(self):
        return self.unlike_news.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", args=[str(self.id)])


class Comment(models.Model):
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE,
        related_name='comments',
        )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    comment = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)

    like_comment = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comment_like')
    unlike_comment = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='comment_unlike')

    def total_likes_comment(self):
        return self.like_comment.count()

    def total_unlikes_comment(self):
        return self.unlike_comment.count()

    class Meta:
        ordering = ['-created_on']
    

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.author)

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.news.id)])



