# Generated by Django 2.0.4 on 2018-04-25 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elephant', '0003_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='in_reply_to_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elephant.Status'),
        ),
    ]