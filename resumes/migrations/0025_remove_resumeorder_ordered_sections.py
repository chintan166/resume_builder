# Generated by Django 4.2.17 on 2025-02-09 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0024_delete_uploadedresume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resumeorder',
            name='ordered_sections',
        ),
    ]
