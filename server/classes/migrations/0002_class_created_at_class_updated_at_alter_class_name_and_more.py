# Generated by Django 5.1.2 on 2024-11-26 14:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
