# Generated by Django 2.1.2 on 2018-12-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181204_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinolimp',
            name='entrance_to_olimp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userinolimp',
            name='last_visit',
            field=models.DateTimeField(null=True),
        ),
    ]
