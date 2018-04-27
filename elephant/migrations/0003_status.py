# Generated by Django 2.0.4 on 2018-04-25 21:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('elephant', '0002_auto_20180421_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('sensitive', models.BooleanField(default=False)),
                ('spoiler_text', models.CharField(default='', max_length=255)),
                ('visibility', models.CharField(choices=[('direct', 'direct'), ('private', 'private'), ('unlisted', 'unlisted'), ('public', 'public')], default='public', max_length=255)),
                ('idempotency_key', models.CharField(default='', max_length=255)),
                ('in_reply_to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephant.Status')),
            ],
        ),
    ]