# Generated by Django 2.1.2 on 2018-12-09 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20181208_0131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinolimp',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserInOlimp',
        ),
    ]
