# Generated by Django 2.0.6 on 2018-07-27 22:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0009_auto_20180720_1049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='them',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='us',
        ),
        migrations.AddField(
            model_name='user',
            name='access_requests',
            field=models.ManyToManyField(related_name='hopefuls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='blocking',
            field=models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='may_access',
            field=models.ManyToManyField(related_name='confidantes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='moved_to',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
    ]