# Generated by Django 4.2.7 on 2023-12-01 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='freeword',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='フリーワード'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='jobs',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='職種'),
        ),
    ]
