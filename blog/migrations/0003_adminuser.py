# Generated by Django 3.0.5 on 2020-07-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200717_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=50)),
                ('author_name', models.CharField(max_length=25)),
                ('join_date', models.DateField()),
            ],
        ),
    ]