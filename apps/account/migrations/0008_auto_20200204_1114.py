# Generated by Django 2.2.9 on 2020-02-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200203_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
