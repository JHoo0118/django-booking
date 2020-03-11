# Generated by Django 2.2.5 on 2020-03-11 19:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_auto_20200307_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='room_photos', verbose_name='이미지'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='baths',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)], verbose_name='욕실'),
        ),
        migrations.AlterField(
            model_name='room',
            name='bedrooms',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)], verbose_name='침실'),
        ),
        migrations.AlterField(
            model_name='room',
            name='beds',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)], verbose_name='침대'),
        ),
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.IntegerField(help_text='몇 명이 머무를 예정입니까?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)], verbose_name='게스트'),
        ),
        migrations.AlterField(
            model_name='room',
            name='instant_book',
            field=models.BooleanField(default=False, verbose_name='즉시예약'),
        ),
    ]
