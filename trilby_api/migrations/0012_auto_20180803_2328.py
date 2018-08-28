# Generated by Django 2.0.6 on 2018-08-03 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trilby_api', '0011_remove_user_may_access'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='access_requests',
            field=models.ManyToManyField(related_name='hopefuls', to='trilby_api.Person'),
        ),
        migrations.AlterField(
            model_name='user',
            name='blocking',
            field=models.ManyToManyField(blank=True, related_name='blocked', to='trilby_api.Person'),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='trilby_api.Person'),
        ),
    ]
