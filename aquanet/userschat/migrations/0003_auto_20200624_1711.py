# Generated by Django 3.0.3 on 2020-06-25 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userschat', '0002_thread_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='notify_first_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='thread',
            name='notify_second_user',
            field=models.BooleanField(default=False),
        ),
    ]
