# Generated by Django 3.1.5 on 2021-04-02 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210403_0101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.IntegerField(default=0)),
                ('cnf_no', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
