# Generated by Django 3.0.8 on 2022-07-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_esigndocument_num_of_signatures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signdocument',
            name='num_of_signatures',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
