# Generated by Django 2.0.6 on 2018-06-09 20:54

from django.db import migrations, models
import trilby_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0003_remove_user_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='url',
            new_name='linked_url',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, upload_to=trilby_api.models.avatar_upload_to),
        ),
        migrations.AlterField(
            model_name='user',
            name='header',
            field=models.ImageField(default=None, upload_to=trilby_api.models.header_upload_to),
        ),
    ]
