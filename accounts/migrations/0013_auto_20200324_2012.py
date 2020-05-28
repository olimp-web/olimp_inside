# Generated by Django 2.1.2 on 2020-03-24 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Profile')),
                ('position', models.CharField(choices=[('boss', 'Руководитель'), ('master', 'Мастер'), ('member', 'Участник'), ('guest', 'Гость')], default='guest', max_length=30)),
                ('room', models.CharField(blank=True, choices=[('501', 'Лекционная'), ('511', 'Коворкинг'), ('512', 'Мастерская')], max_length=3, null=True)),
            ],
            bases=('accounts.profile',),
        )
    ]
