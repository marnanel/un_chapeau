# Generated by Django 2.0.5 on 2018-05-28 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0002_auto_20180526_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
    ]
