# Generated by Django 4.2.2 on 2023-12-19 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_skill_category_skill_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
