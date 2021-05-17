# Generated by Django 3.2 on 2021-05-15 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='static/images/news/news/')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like_news', models.ManyToManyField(blank=True, related_name='the_news', to=settings.AUTH_USER_MODEL)),
                ('unlike_news', models.ManyToManyField(blank=True, related_name='the_news_unlike', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'permissions': [('all', 'all of the permissions')],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like_comment', models.ManyToManyField(blank=True, related_name='comment_like', to=settings.AUTH_USER_MODEL)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.news')),
                ('unlike_comment', models.ManyToManyField(blank=True, related_name='comment_unlike', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
