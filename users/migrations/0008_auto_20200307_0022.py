# Generated by Django 2.2.5 on 2020-03-06 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200302_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=200, verbose_name='자기소개'),
        ),
    ]
