# Generated by Django 4.1.7 on 2023-04-10 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0003_alter_userinfo_password_alter_userinfo_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
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
                ("news_name", models.CharField(max_length=64, verbose_name="新闻")),
                ("news_time", models.DateTimeField(verbose_name="新闻时间")),
                ("news_num", models.IntegerField(verbose_name="新闻评论数")),
            ],
        ),
        migrations.CreateModel(
            name="NewsData",
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
                ("ip_territory", models.CharField(max_length=16, verbose_name="ip属地")),
                ("comment_time", models.DateTimeField(verbose_name="评论时间")),
                ("comment_text", models.CharField(max_length=128, verbose_name="评论内容")),
                (
                    "news",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.news"
                    ),
                ),
            ],
        ),
    ]
