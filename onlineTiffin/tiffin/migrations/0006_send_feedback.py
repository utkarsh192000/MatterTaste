# Generated by Django 2.2.6 on 2020-04-26 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiffin', '0005_delete_send_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send_Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message1', models.TextField(null=True)),
                ('date', models.CharField(max_length=30, null=True)),
                ('signup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tiffin.Signup')),
            ],
        ),
    ]
