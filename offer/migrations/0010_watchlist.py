# Generated by Django 5.1.5 on 2025-01-22 23:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0009_alter_offer_supervisor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
