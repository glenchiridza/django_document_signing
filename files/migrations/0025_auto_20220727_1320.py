# Generated by Django 3.0.8 on 2022-07-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0024_auto_20220727_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signdocument',
            name='signed_by',
            field=models.CharField(default='glenc', max_length=300),
        ),
    ]