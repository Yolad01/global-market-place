# Generated by Django 4.2.2 on 2023-10-28 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_clientprofile_services_needed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('attach_files', models.FileField(blank=True, null=True, upload_to='project_description_files')),
                ('budget', models.IntegerField(blank=True, max_length=6)),
                ('budget_flexible', models.BooleanField(default=False)),
                ('date', models.DateTimeField()),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]