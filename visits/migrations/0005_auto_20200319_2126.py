# Generated by Django 2.1.2 on 2020-03-19 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0004_merge_20200319_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='leave_timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время выхода'),
        ),
    ]
