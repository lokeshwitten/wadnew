# Generated by Django 3.1.5 on 2021-05-05 07:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0008_restaurant_reserve_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='reserve_list',
            field=models.CharField(default=[], max_length=200, null=True, validators=[django.core.validators.int_list_validator]),
        ),
    ]
