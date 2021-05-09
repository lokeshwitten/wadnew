# Generated by Django 3.1.5 on 2021-05-09 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoteladmin', '0024_restaurant_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_rating', models.IntegerField(default=3)),
                ('food_rating', models.IntegerField(default=3)),
                ('service_rating', models.IntegerField(default=3)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='feedback',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hoteladmin.feedback'),
        ),
    ]
