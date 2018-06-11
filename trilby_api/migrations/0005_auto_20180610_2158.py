# Generated by Django 2.0.6 on 2018-06-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0004_auto_20180609_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='visibility',
            field=models.CharField(choices=[('P', 'public'), ('X', 'private'), ('U', 'unlisted'), ('D', 'direct')], default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_visibility',
            field=models.CharField(choices=[('P', 'public'), ('X', 'private'), ('U', 'unlisted'), ('D', 'direct')], default='P', max_length=1),
        ),
    ]
