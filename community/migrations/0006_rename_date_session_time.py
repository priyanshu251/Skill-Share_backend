# Generated by Django 5.0.4 on 2024-05-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0005_alter_community_banner_alter_community_profile_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="session",
            old_name="date",
            new_name="time",
        ),
    ]
