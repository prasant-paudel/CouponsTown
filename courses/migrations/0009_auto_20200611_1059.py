# Generated by Django 3.0.7 on 2020-06-11 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
