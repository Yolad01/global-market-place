# Generated by Django 4.2.2 on 2023-11-26 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_inbox_sender_alter_inbox_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='message',
        ),
    ]