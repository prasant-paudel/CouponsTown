# Generated by Django 3.0.7 on 2020-06-18 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_course_affiliate_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='affiliate_url',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
