# Generated by Django 2.2.8 on 2020-02-03 12:34

import apps.post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20200203_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractiontemplate',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=apps.post.models.UserActionTemplate.upload_path),
        ),
    ]