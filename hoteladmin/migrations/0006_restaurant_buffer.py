# Generated by Django 3.1.5 on 2021-05-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0005_auto_20210504_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='buffer',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
