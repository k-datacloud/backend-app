# Generated by Django 4.2.7 on 2023-12-17 07:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0017_post_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='likedPosts',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='userapp.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
