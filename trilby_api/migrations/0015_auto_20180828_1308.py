# Generated by Django 2.1 on 2018-08-28 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0014_user_actor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='blocking',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
    ]
