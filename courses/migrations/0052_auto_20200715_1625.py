# Generated by Django 3.0.7 on 2020-07-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0051_auto_20200713_0741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['expired', 'name']},
        ),
        migrations.AddField(
            model_name='course',
            name='urlbox',
            field=models.TextField(null=True),
        ),
    ]
