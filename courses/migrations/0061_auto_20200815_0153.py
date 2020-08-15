# Generated by Django 3.1 on 2020-08-15 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0060_auto_20200811_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name_base64',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='name_encoded',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
