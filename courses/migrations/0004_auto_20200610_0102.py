# Generated by Django 3.0.7 on 2020-06-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20200610_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='platform',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
