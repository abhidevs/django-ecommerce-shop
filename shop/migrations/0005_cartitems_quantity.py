# Generated by Django 3.0.5 on 2020-06-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
