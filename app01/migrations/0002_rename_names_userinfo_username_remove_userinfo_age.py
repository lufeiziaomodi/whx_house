# Generated by Django 4.1.7 on 2023-03-29 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userinfo", old_name="names", new_name="username",
        ),
        migrations.RemoveField(model_name="userinfo", name="age",),
    ]
