# Generated by Django 5.1.2 on 2024-11-27 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_or_lab_id', models.IntegerField()),
                ('sender_id', models.CharField(max_length=10)),
                ('notice_type', models.CharField(choices=[('class', 'Class'), ('lab', 'Lab')], max_length=10)),
                ('post_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('content_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('completion_time', models.DateTimeField()),
                ('notice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notices.notice')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField()),
                ('notice_content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notices.noticecontent')),
                ('notice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notices.notice')),
            ],
            options={
                'unique_together': {('notice_id', 'notice_content_id')},
            },
        ),
        migrations.CreateModel(
            name='NoticeContentTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notices.noticecontent')),
                ('notice_tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notices.noticetag')),
            ],
            options={
                'unique_together': {('notice_content_id', 'notice_tag_id')},
            },
        ),
    ]