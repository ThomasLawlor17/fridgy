# Generated by Django 4.0.4 on 2022-05-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_food_category_alter_food_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='count',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
