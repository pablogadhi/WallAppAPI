# Generated by Django 3.1.1 on 2020-09-24 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['time']},
        ),
    ]