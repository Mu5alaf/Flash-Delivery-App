# Generated by Django 4.2.7 on 2023-11-24 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlashDS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='pickup_address',
            field=models.CharField(blank=True, max_length=225),
        ),
        migrations.AddField(
            model_name='request',
            name='pickup_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='pickup_lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='pickup_phone',
            field=models.CharField(blank=True, max_length=45),
        ),
    ]
