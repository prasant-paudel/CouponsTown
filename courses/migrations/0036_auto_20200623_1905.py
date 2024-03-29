# Generated by Django 3.0.7 on 2020-06-23 13:20

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0035_course_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('NOT SET', 'not_set'), ('DEVELOPMENT', 'development'), ('IT & SOFTWARE', 'it&software'), ('OFFICE & PRODUCTIVITY', 'office&productivity'), ('DESIGN & PHOTOGRAPHY', 'design&photography'), ('MARKETING & BUSINESS', 'marketing&business'), ('OTHERS', 'others')], max_length=104),
        ),
    ]
