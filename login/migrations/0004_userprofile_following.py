# Generated by Django 5.2 on 2025-04-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='login.userprofile'),
        ),
    ]
