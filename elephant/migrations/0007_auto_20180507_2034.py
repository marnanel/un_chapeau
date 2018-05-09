# Generated by Django 2.0.4 on 2018-05-07 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephant', '0006_auto_20180505_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(default='/static/un_chapeau/defaults/avatar_1.jpg', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='default_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='default_visibility',
            field=models.CharField(choices=[(0, 'private'), (1, 'unlisted'), (2, 'public'), (3, 'direct')], default=2, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='header',
            field=models.CharField(default='/static/un_chapeau/defaults/avatar_1.jpg', max_length=255),
        ),
        migrations.AlterField(
            model_name='status',
            name='visibility',
            field=models.CharField(choices=[(0, 'private'), (1, 'unlisted'), (2, 'public'), (3, 'direct')], default=2, max_length=255),
        ),
    ]