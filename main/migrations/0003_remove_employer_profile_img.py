# Generated by Django 4.2.2 on 2023-07-26 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='profile_img',
        ),
    ]
