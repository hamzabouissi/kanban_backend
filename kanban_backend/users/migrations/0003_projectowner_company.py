# Generated by Django 3.1.13 on 2022-01-03 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220101_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectowner',
            name='company',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
