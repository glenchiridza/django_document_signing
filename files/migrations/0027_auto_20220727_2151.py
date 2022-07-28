# Generated by Django 3.0.8 on 2022-07-27 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0026_auto_20220727_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendforsigning',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]