# Generated by Django 4.1.3 on 2022-11-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_tl',
            field=models.BooleanField(default=False),
        ),
    ]
