# Generated by Django 2.0.6 on 2018-07-18 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0006_auto_20180619_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar',
            new_name='_avatar',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='header',
            new_name='_header',
        ),
    ]
