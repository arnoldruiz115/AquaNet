# Generated by Django 3.0.3 on 2020-04-30 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(blank=True, max_length=200)),
                ('species', models.CharField(max_length=200)),
                ('max_size', models.FloatField()),
                ('water_type', models.CharField(max_length=50)),
                ('for_sale', models.BooleanField(default=False)),
                ('price', models.FloatField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('thumbnail', models.ImageField(blank=True, default=None, upload_to='species-images')),
                ('thumbnail_aspect_ratio', models.FloatField(blank=True, default=None, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='species-images')),
                ('order', models.IntegerField(default=-1)),
                ('aspect_ratio', models.FloatField(blank=True, default=None, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='speciesprofile.Profile')),
            ],
        ),
    ]
