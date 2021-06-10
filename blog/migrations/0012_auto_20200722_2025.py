# Generated by Django 3.0.5 on 2020-07-22 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200720_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft_status',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]