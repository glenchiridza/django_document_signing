# Generated by Django 3.0.8 on 2022-07-26 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0014_sendforsigning_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendforsigning',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='signdocument',
            name='signature',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.Signature'),
        ),
    ]
