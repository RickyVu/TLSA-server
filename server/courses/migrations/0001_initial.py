# Generated by Django 5.1.2 on 2024-12-23 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=8, verbose_name='Course Code')),
                ('course_sequence', models.CharField(max_length=5, verbose_name='Course Sequence')),
                ('department', models.CharField(max_length=50, verbose_name='Department')),
                ('name', models.CharField(max_length=100, verbose_name='Course Name')),
            ],
            options={
                'db_table': 'course',
                'unique_together': {('course_code', 'course_sequence')},
            },
        ),
        migrations.CreateModel(
            name='CourseClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_instance', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='courses.course')),
            ],
            options={
                'db_table': 'course_class',
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course')),
            ],
            options={
                'db_table': 'course_enrollment',
            },
        ),
    ]
