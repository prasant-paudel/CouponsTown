# Generated by Django 3.0.7 on 2020-06-21 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_auto_20200621_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realdiscount',
            name='coupon',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='realdiscount',
            name='platform',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
