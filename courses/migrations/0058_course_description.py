# Generated by Django 3.0.7 on 2020-08-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0057_auto_20200728_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.BinaryField(blank=True),
        ),
    ]