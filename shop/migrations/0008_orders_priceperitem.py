# Generated by Django 3.0.5 on 2020-07-03 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='pricePerItem',
            field=models.IntegerField(default=0),
        ),
    ]
