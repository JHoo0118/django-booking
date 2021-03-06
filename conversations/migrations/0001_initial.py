# Generated by Django 2.2.5 on 2020-01-23 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('participants', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='참가자')),
            ],
            options={
                'verbose_name': '대화방',
                'verbose_name_plural': '대화방',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(verbose_name='메세지')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversations.Conversation', verbose_name='대화방')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '메세지',
                'verbose_name_plural': '메세지',
            },
        ),
    ]
