# Generated by Django 4.1.7 on 2023-03-25 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("names", models.CharField(max_length=32)),
                ("password", models.CharField(max_length=32)),
                ("age", models.IntegerField()),
            ],
        ),
    ]
