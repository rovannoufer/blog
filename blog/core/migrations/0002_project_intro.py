# Generated by Django 5.0 on 2023-12-14 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='intro',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
