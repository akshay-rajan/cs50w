# Generated by Django 4.2.7 on 2023-11-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0002_post_like_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.CharField(max_length=300),
        ),
    ]