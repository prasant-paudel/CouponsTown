# Generated by Django 3.1 on 2021-02-07 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0063_course_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='last_updated',
        ),
    ]