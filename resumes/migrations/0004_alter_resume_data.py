# Generated by Django 4.2.17 on 2025-02-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0003_alter_resume_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]
