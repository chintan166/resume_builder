# Generated by Django 4.2.17 on 2025-02-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0013_resumeorder_company_name_resumeorder_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeorder',
            name='certifications',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resumeorder',
            name='interest',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resumeorder',
            name='languages',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resumeorder',
            name='skills',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
