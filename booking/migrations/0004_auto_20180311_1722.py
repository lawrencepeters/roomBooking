# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-11 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20180311_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinghistory',
            options={'verbose_name': 'Booking History', 'verbose_name_plural': 'Booking History'},
        ),
    ]
