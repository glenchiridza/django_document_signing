# Generated by Django 3.0.8 on 2022-07-27 11:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0016_signdocument_signed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signdocument',
            name='signed_by',
        ),
        migrations.AddField(
            model_name='signdocument',
            name='signed_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
