# Generated by Django 2.2.6 on 2020-04-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffin', '0002_auto_20200425_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
