# Generated by Django 2.2.8 on 2020-01-10 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=None, related_name='topics', to='channel.Channel')),
            ],
        ),
    ]
