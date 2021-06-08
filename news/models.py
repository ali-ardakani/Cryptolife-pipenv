from django.contrib.auth.models import User
from config.settings import AUTH_USER_MODEL
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.db import models
from django.urls import  reverse
from ckeditor.fields import  RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    slug = models.CharField(max_length=300)


    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("news_new")


def get_header_image_filepath(self, filepath):
    return f'images/news/header/{self.author.id}/{self.header_image}'


class News(models.Model):

    class Meta:
        permissions = [
            ('all', 'all of the permissions')
        ]
        ordering = ['-datetime']

    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to=get_header_image_filepath)
    body = RichTextUploadingField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ManyToManyField(Category, default='cryptocurrency', related_name='category')
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
    comment = RichTextUploadingField()
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


# class Google_News(models.Model):

#     class Meta:
#         permissions = [
#             ('all', 'all of the permissions')
#         ]
#         ordering = ['-date_time']

#     title = models.CharField(max_length=355)
#     site = models.CharField(max_length=255)
#     description = models.TextField()
#     date_time = models.DateTimeField()
#     image = models.URLField(null=True, blank=True)
#     category = models.ManyToManyField(Category, related_name='category_google_news')

#     def __str__(self):
#         return self.title


