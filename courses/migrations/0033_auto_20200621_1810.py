# Generated by Django 3.0.7 on 2020-06-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_realdiscount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realdiscount',
            name='title',
        ),
        migrations.AlterField(
            model_name='realdiscount',
            name='valid',
            field=models.BooleanField(default=True),
        ),
    ]
