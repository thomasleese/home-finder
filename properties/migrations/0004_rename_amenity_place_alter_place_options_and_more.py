# Generated by Django 4.0.6 on 2022-07-29 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0003_alter_amenity_options_alter_property_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Amenity",
            new_name="Place",
        ),
        migrations.AlterModelOptions(
            name="place",
            options={},
        ),
        migrations.AddField(
            model_name="property",
            name="google_place_id",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
    ]