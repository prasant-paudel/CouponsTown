# Generated by Django 3.0.7 on 2020-06-18 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0023_auto_20200618_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
