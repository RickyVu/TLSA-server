# Generated by Django 5.1.2 on 2024-12-17 17:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(db_column='student_user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id', verbose_name='Student'),
        ),
        migrations.AlterUniqueTogether(
            name='courseclass',
            unique_together={('course', 'class_instance')},
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together={('student', 'course')},
        ),
    ]