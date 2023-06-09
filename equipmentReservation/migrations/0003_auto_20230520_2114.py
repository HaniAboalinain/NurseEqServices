# Generated by Django 3.0 on 2023-05-20 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipmentReservation', '0002_equipmentreservation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentreservation',
            name='card_number',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{14}$')]),
        ),
        migrations.AddField(
            model_name='equipmentreservation',
            name='cvv',
            field=models.CharField(blank=True, max_length=3, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{3}$')]),
        ),
        migrations.AddField(
            model_name='equipmentreservation',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('visa', 'Visa')], default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmentreservation',
            name='visa_exp_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
