# Generated by Django 5.0.4 on 2024-04-13 21:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeper', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='card_type',
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='expiration_date',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card', to=settings.AUTH_USER_MODEL),
        ),
    ]