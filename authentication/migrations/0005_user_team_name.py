# Generated by Django 4.1.3 on 2022-11-14 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_is_tl'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team_name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
