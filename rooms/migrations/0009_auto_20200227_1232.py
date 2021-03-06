# Generated by Django 2.2.5 on 2020-02-27 03:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_auto_20200218_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='baths',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='욕실'),
        ),
        migrations.AlterField(
            model_name='room',
            name='bedrooms',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='침실'),
        ),
        migrations.AlterField(
            model_name='room',
            name='beds',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='침대'),
        ),
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.IntegerField(help_text='몇 명이 머무를 예정입니까?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='게스트'),
        ),
    ]
