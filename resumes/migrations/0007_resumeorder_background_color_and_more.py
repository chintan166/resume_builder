# Generated by Django 4.2.17 on 2025-02-07 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0006_resumeorder_created_at_resumeorder_ordered_sections_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeorder',
            name='background_color',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='resumeorder',
            name='border_style',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='resumeorder',
            name='font_style',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
