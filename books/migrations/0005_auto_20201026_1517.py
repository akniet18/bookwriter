# Generated by Django 3.1.2 on 2020-10-26 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]