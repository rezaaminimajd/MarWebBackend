# Generated by Django 2.2.8 on 2020-02-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_auto_20200203_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='subject',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
