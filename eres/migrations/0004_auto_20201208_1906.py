# Generated by Django 3.1.4 on 2020-12-08 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eres', '0003_auto_20201207_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='file',
        ),
    ]