# Generated by Django 4.0.4 on 2022-05-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_food_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.CharField(default='https://i.imgur.com/G4NNtuW.png', max_length=200),
        ),
    ]
