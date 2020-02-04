# Generated by Django 2.2.9 on 2020-02-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20200204_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('follow_user', 'follow user'), ('follow_channel', 'follow channel'), ('like', 'like'), ('post', 'new post'), ('comment', 'new comment')], max_length=20),
        ),
    ]
