# Generated by Django 3.1.5 on 2021-05-09 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0025_auto_20210510_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='app_message',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='feedback',
            name='food_message',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='service_rating',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
