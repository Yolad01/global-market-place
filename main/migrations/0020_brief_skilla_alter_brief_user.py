# Generated by Django 4.2.2 on 2023-10-28 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_jobcategory_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='brief',
            name='skilla',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skilla', to='main.skillas'),
        ),
        migrations.AlterField(
            model_name='brief',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='main.clients'),
        ),
    ]