# Generated by Django 3.1.2 on 2020-10-23 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20201014_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
