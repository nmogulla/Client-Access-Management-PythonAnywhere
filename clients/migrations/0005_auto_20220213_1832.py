# Generated by Django 3.0.1 on 2022-02-14 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20220213_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='VIN_number',
            field=models.CharField(default=' ', max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='date_of_last_service',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='date_of_purchase',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='make',
            field=models.CharField(default=' ', max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
