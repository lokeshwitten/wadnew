# Generated by Django 3.1.5 on 2021-05-04 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0004_auto_20210503_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hoteladmin.restaurant'),
        ),
    ]
