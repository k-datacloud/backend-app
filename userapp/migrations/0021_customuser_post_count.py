# Generated by Django 4.2.7 on 2023-12-21 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0020_alter_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='post_count',
            field=models.IntegerField(default=0, verbose_name='投稿数'),
        ),
    ]