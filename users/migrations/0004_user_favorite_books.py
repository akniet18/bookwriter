# Generated by Django 3.1.2 on 2020-10-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20201026_1517'),
        ('users', '0003_auto_20201023_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_books',
            field=models.ManyToManyField(related_name='fav', to='books.Book'),
        ),
    ]