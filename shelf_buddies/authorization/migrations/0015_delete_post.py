# Generated by Django 4.2.3 on 2023-12-03 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0014_remove_post_book'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]