# Generated by Django 4.0.6 on 2022-07-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("searches", "0004_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="search",
            name="min_number_of_bedrooms",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
