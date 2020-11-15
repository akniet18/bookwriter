# Generated by Django 3.1.2 on 2020-11-13 16:58

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_track'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranges', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), size=None)),
                ('color', models.CharField(max_length=50)),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.text')),
            ],
        ),
    ]