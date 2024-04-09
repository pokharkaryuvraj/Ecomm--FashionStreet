# Generated by Django 5.0 on 2023-12-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('branch', models.CharField(max_length=20)),
                ('percent', models.FloatField()),
            ],
        ),
    ]
