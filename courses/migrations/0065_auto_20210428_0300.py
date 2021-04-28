# Generated by Django 3.1 on 2021-04-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0064_remove_course_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.AddField(
            model_name='course',
            name='image_url',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]