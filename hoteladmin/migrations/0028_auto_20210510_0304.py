# Generated by Django 3.1.5 on 2021-05-09 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0027_auto_20210510_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='feedback',
        ),
        migrations.AddField(
            model_name='feedback',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='hoteladmin.order'),
        ),
    ]
