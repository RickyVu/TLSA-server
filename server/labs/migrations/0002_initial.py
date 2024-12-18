# Generated by Django 5.1.2 on 2024-12-17 17:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='managelab',
            name='manager',
            field=models.ForeignKey(db_column='manager_user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id'),
        ),
    ]
